import json
import logging
import os
from typing import Optional
from kafka import KafkaProducer
from utils.env_config import config


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

        """
        self._service_uri = service_uri
        self._ca_path = ca_path
        self._cert_path = cert_path
        self._key_path = key_path

    def __enter__(self):
        self._producer = KafkaProducer(
            bootstrap_servers=self._service_uri,
            security_protocol="SSL",
            ssl_cafile=self._ca_path,
            ssl_certfile=self._cert_path,
            ssl_keyfile=self._key_path,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )

    @property
    def producer(self):
        """Access to genuine Kafka producer"""
        return self._producer

    def send(self, topic: str, value, timeout=None, *args, **kwargs) -> None:
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
        self._producer.close()


# _kafka_url = config['Metrics endpoint']['Aiven']['Kafka']['host']
# _kafka_port = str(config['Metrics endpoint']['Aiven']['Kafka']['port'])
# kafka_uri = ':'.join((_kafka_url, _kafka_port))
# ca_path = os.environ['CA-CERT']
# cert_path = os.environ['SERVICE_CERT']
# key_path = os.environ['SERVICE-KEY']
#
# aiven_kafka_producer = Producer(kafka_uri, ca_path, cert_path, key_path)
# with aiven_kafka_producer:
#     aiven_kafka_producer.send('website-metrics', value={'message': '5'})
# print('')
