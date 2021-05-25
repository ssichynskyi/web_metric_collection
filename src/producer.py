import json
import logging

from kafka import KafkaProducer


log = logging.getLogger(__name__)


# here I've used a code example from here:
# https://github.com/aiven/aiven-examples/blob/master/kafka/python/producer_example.py


class Producer:
    def __init__(self, service_uri: str, ca_path: str, cert_path: str, key_path: str):
        """Class for creating Kafka producer

        Args:
            service_uri: uri to active Kafka broker service
            ca_path: path to CA certificate
            cert_path: service cert path
            key_path: service cert key path

        Usage:
            Connection is activated not on object instantiation but
            when entering with statement. e.g.:
            producer = Producer(...)
            with producer:
                producer.send(...)

        """
        self._service_uri = service_uri
        self._ca_path = ca_path
        self._cert_path = cert_path
        self._key_path = key_path

    def __enter__(self):
        """Initializes connection to broker on entering with block."""
        self._producer = KafkaProducer(
            bootstrap_servers=self._service_uri,
            security_protocol="SSL",
            ssl_cafile=self._ca_path,
            ssl_certfile=self._cert_path,
            ssl_keyfile=self._key_path,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        log.info(f'Connected to kafka broker at: {self._service_uri}')

    @property
    def producer(self):
        """Access to genuine Kafka producer."""
        return self._producer

    def send(self, topic: str, value, *args, timeout=None, **kwargs) -> None:
        """Sends msg to a topic

        Args:
            topic: topic to post to
            value: value to post. Byte or serializable.
            timeout: timeout in seconds
            *args:
            **kwargs:

        Returns:
            None

        Raises:
            KafkaTimeoutError: if unable to fetch topic metadata, or unable
                to obtain memory buffer prior to configured max_block_ms

        """
        log.info(f'Sending message {value} to topic {topic}')
        self._producer.send(topic, value, *args, **kwargs)
        self._producer.flush(timeout)

    def __exit__(self, exc_type, exc_value, traceback):
        """Finalizer which is called on exit with block."""
        self._producer.close()
