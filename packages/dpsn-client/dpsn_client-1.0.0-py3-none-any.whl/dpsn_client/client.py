import paho.mqtt.client as mqtt
from web3 import Web3
from eth_account.messages import encode_defunct
from enum import Enum
from typing import Optional, Dict, Any
from events import Events
import json
import ssl
import time
import os
import logging
import threading

logger = logging.getLogger("DpsnClient")

class DPSN_ERROR_CODES(Enum):
    CONNECTION_ERROR = 400
    UNAUTHORIZED = 401
    PUBLISH_ERROR = 402
    INITIALIZATION_FAILED = 403
    CLIENT_NOT_INITIALIZED = 404
    CLIENT_NOT_CONNECTED = 405
    SUBSCRIBE_ERROR = 406
    SUBSCRIBE_NO_GRANT = 407
    SUBSCRIBE_SETUP_ERROR = 408
    DISCONNECT_ERROR = 409
    BLOCKCHAIN_CONFIG_ERROR = 410
    INVALID_PRIVATE_KEY = 411
    ETHERS_ERROR = 412
    MQTT_ERROR = 413
    MESSAGE_HANDLING_ERROR = 414

class DPSNError(Exception):
    def __init__(self, code: DPSN_ERROR_CODES, message: str, status: Optional[str] = None):
        self.code = code
        self.message = message
        self.status = status
        super().__init__(self.message)

    def to_dict(self):
        return {
            'code': self.code.value,
            'message': self.message,
            'status': self.status
        }

    def __str__(self):
        return str(self.to_dict())

class DpsnClient(Events):
    __events__ = ('on_msg', 'on_error')

    def __init__(self, dpsn_url: str, private_key: str, chain_options: Dict[str, Any], connection_options: Dict[str, Any] = None):
        super().__init__()
        connection_options = connection_options or {}
        self.web3 = Web3()
        self.validate_private_key(private_key)
        account = self.web3.eth.account.from_key(private_key)
        self.account = account
        self.wallet_address = account.address
        self.mainnet = chain_options.get('network') == 'mainnet'
        self.testnet = chain_options.get('network') == 'testnet'
        self.blockchain_type = chain_options.get('wallet_chain_type')
        self.hostname = dpsn_url
        self.secure = connection_options.get('ssl', True)
        self.full_url = f"{'mqtts' if self.secure else 'mqtt'}://{self.hostname}"
        self.dpsn_broker = None
        self.connected = False
        self._init_done = False
        self._connect_event = threading.Event()
        self._validate_initialization(chain_options)

    def _validate_initialization(self, chain_options: Dict[str, Any]) -> None:
        if chain_options.get('network') not in ['mainnet', 'testnet']:
            raise ValueError('Network must be either mainnet or testnet')
        if chain_options.get('wallet_chain_type') != 'ethereum':
            raise ValueError('Only Ethereum wallet_chain_type is supported')

    def validate_private_key(self, private_key: str) -> None:
        try:
            clean_key = private_key.replace('0x', '')
            if not (len(clean_key) == 64 and all(c in '0123456789abcdefABCDEF' for c in clean_key)):
                raise ValueError("Invalid private key format")
            self.web3.eth.account.from_key(private_key)
        except Exception as e:
            raise DPSNError(DPSN_ERROR_CODES.INVALID_PRIVATE_KEY, f"Invalid private key: {str(e)}", "disconnected")

    def init(self, options: Dict[str, Any] = None) -> mqtt.Client:
        if self._init_done and self.dpsn_broker and self.dpsn_broker.is_connected():
            logger.info("Already initialized and connected.")
            return self.dpsn_broker

        options = options or {}
        message = "testing"
        signature = self.account.sign_message(encode_defunct(text=message))
        self.password = signature.signature.hex()

        self.dpsn_broker = mqtt.Client(protocol=mqtt.MQTTv5)
        self.dpsn_broker.username_pw_set(username=self.wallet_address, password=self.password)
        self.dpsn_broker.connect_timeout = options.get('connect_timeout', 5000)
        self.dpsn_broker.clean_session = True

        def on_connect(client, userdata, flags, rc, properties=None):
            if rc == 0:
                self.connected = True
                self._connect_event.set()
                logger.info("Successfully connected to MQTT broker")
            else:
                self.connected = False
                self._connect_event.set()
                logger.error(f"Connection failed with code: {rc}")

        def on_disconnect(client, userdata, rc, properties=None):
            self.connected = False
            logger.warning(f"Disconnected with result code: {rc}")

        def on_message(client, userdata, msg):
            try:
                payload = msg.payload.decode("utf-8")
                try:
                    payload = json.loads(payload)
                except json.JSONDecodeError:
                    pass
                self.on_msg({'topic': msg.topic, 'payload': payload})
            except Exception as e:
                error = DPSNError(DPSN_ERROR_CODES.MESSAGE_HANDLING_ERROR, str(e), "connected")
                self.on_error(error)

        self.dpsn_broker.on_connect = on_connect
        self.dpsn_broker.on_disconnect = on_disconnect
        self.dpsn_broker.on_message = on_message

        self._connect_with_retry(options.get('retry_options', {}))
        self._init_done = True
        return self.dpsn_broker

    def _connect_with_retry(self, retry_options: Dict[str, Any]) -> None:
        max_retries = retry_options.get('max_retries', 3)
        initial_delay = retry_options.get('initial_delay', 1000) / 1000
        max_delay = retry_options.get('max_delay', 5000) / 1000
        port = 8883 if self.secure else 1883
        if self.secure:
            self.dpsn_broker.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)

        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt + 1} connecting to {self.hostname}:{port}")
                self.dpsn_broker.connect(self.hostname, port=port, keepalive=60)
                self.dpsn_broker.loop_start()
                self._connect_event.wait(timeout=10)
                if self.connected:
                    logger.info("MQTT connection established.")
                    return
                else:
                    raise Exception("MQTT connection failed")
            except Exception as e:
                logger.error(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise DPSNError(DPSN_ERROR_CODES.CONNECTION_ERROR, str(e), "disconnected")
                delay = min(initial_delay * (2 ** attempt), max_delay)
                time.sleep(delay)

    def disconnect(self):
        if not self.dpsn_broker:
            raise DPSNError(DPSN_ERROR_CODES.CLIENT_NOT_INITIALIZED, "Cannot disconnect: client not initialized", "disconnected")
        try:
            self.dpsn_broker.loop_stop()
            self.dpsn_broker.disconnect()
            self.connected = False
        except Exception as e:
            raise DPSNError(DPSN_ERROR_CODES.DISCONNECT_ERROR, str(e), "disconnected")

    def subscribe(self, topic: str, options: Dict[str, Any] = None) -> None:
        if not self.dpsn_broker or not self.dpsn_broker.is_connected():
            raise DPSNError(DPSN_ERROR_CODES.CLIENT_NOT_CONNECTED, "Cannot subscribe: client not connected", "disconnected")
        options = options or {}
        qos = options.get('qos', 1)
        result, mid = self.dpsn_broker.subscribe(topic, qos=qos)
        if result != mqtt.MQTT_ERR_SUCCESS:
            raise DPSNError(DPSN_ERROR_CODES.SUBSCRIBE_ERROR, f"Failed to subscribe to topic '{topic}'", "connected")

    def unsubscribe(self, topic: str) -> None:
        if not self.dpsn_broker or not self.connected:
            raise DPSNError(DPSN_ERROR_CODES.CLIENT_NOT_CONNECTED, "Cannot unsubscribe: client not connected", "disconnected")
        result, mid = self.dpsn_broker.unsubscribe(topic)
        if result != mqtt.MQTT_ERR_SUCCESS:
            raise DPSNError(DPSN_ERROR_CODES.SUBSCRIBE_ERROR, f"Failed to unsubscribe from topic '{topic}'", "connected")

    def publish(self, topic: str, message: Any, options: Dict[str, Any] = None) -> None:
        if not self.dpsn_broker or not self.connected:
            raise DPSNError(DPSN_ERROR_CODES.CLIENT_NOT_CONNECTED, "Cannot publish: client not connected", "disconnected")
        parent_topic = topic.split('/')[0]
        if not parent_topic.startswith('0x'):
            raise ValueError("Invalid topic format: must start with '0x'")
        signature = self.account.sign_message(encode_defunct(text=parent_topic))
        options = options or {}
        properties = mqtt.Properties(mqtt.PacketTypes.PUBLISH)
        properties.UserProperty = [("signature", signature.signature.hex())]
        qos = options.get('qos', 1)
        retain = options.get('retain', False)
        result = self.dpsn_broker.publish(topic, json.dumps(message), qos=qos, retain=retain, properties=properties)
        result.wait_for_publish()

    def generate_topic_hash(self, topic_name: str) -> str:
        nonce = os.urandom(8).hex()
        topic_seed = f"{nonce}_{topic_name}"
        return self.web3.keccak(text=topic_seed).hex()
