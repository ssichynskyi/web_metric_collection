"""Implements wrapper for Kafka Producer."""
import json
import logging

from kafka import KafkaProducer


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


# here I've used a code example from here:
# https://github.com/aiven/aiven-examples/blob/master/kafka/python/producer_example.py


class Producer:
    def __init__(self, **connection_kwargs):
        """Class for creating Kafka producer

        Args:
            *args - positional arguments as taken by KafkaProducer
            **connection_kwargs - keyword arguments as taken by KafkaProducer
            below there are some useful connection_kwargs and their default value:
                'bootstrap_servers' - uri with port for the service
                'security_protocol' - SSL, SASL_PLAINTEXT, etc
                'sasl_mechanism': None,
                'sasl_plain_username': None,
                'sasl_plain_password': None,
                'ssl_cafile': None,
                'ssl_certfile': None,
                'ssl_keyfile': None
            Note:
                although all params are optional, at least
                'sasl_plain_username' and 'sasl_plain_password'
                or
                'ssl_cafile', 'ssl_certfile' and 'ssl_keyfile
                or other certificate-related inputs shall be defined

        Usage:
            Connection is activated not on object instantiation but
            when entering with statement. e.g.:
            producer = Producer(...)
            with producer:
                producer.send(...)

        """
        self._connection_data = connection_kwargs
        try:
            self._connection_data['security_protocol']
        except KeyError:
            username_given = 'sasl_plain_username' in self._connection_data.keys()
            password_given = 'sasl_plain_password' in self._connection_data.keys()
            ca_file_given = 'ssl_cafile' in self._connection_data.keys()
            service_cert_given = 'ssl_certfile' in self._connection_data.keys()
            service_key_given = 'ssl_keyfile' in self._connection_data.keys()
            if all((ca_file_given, service_cert_given, service_key_given)):
                self._connection_data['security_protocol'] = 'SSL'
            elif username_given and password_given:
                self._connection_data['security_protocol'] = 'SASL_PLAINTEXT'
            else:
                msg = 'Security protocol not provided and cannot be determined automatically.'
                msg = f'{msg} Check auth kwargs'
                raise ValueError(msg)
        self._producer = None

    def __enter__(self):
        """Initializes connection to broker on entering with block."""
        self._producer = KafkaProducer(
            **self._connection_data,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        log.info(f'Connected to kafka broker at: {self._producer.config["bootstrap_servers"]}')

    @property
    def producer(self):
        """Access to genuine Kafka producer."""
        return self._producer

    def send(self, topic: str, value, *args, timeout=None, **kwargs) -> None:
        """Sends msg to a topic.

        Args:
            topic: topic to post to
            value: value to post. Byte or serializable.
            *args: positional args
            timeout: timeout in seconds
            **kwargs: keyword args

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
