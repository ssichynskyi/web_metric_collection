"""Runs metrics_collector and Kafka producer collaboratively."""
import argparse
import logging
import os
import time

from typing import Optional

try:
    from ..src.metrics_collector import get_metrics
    from ..src.producer import Producer
    from ..utils.env_config import config
except ImportError:
    from src.metrics_collector import get_metrics
    from src.producer import Producer
    from utils.env_config import config


# set default params
TOPIC = 'website-metrics'
SLEEP_BETWEEN_REQUESTS = config['Monitored web sites']['monedo']['request sleep']
TARGET_URL = config['Monitored web sites']['monedo']['url']
TARGET_PATTERN = config['Monitored web sites']['monedo']['expected pattern']

_collection_provider = os.environ['BROKER_SERVICE_PROVIDER']
_broker_settings = config['Metrics collection endpoint'][_collection_provider]['broker']
_broker_type = _broker_settings['type']
_broker_url = _broker_settings['host']
_broker_port = str(_broker_settings['port'])
_broker_uri = ':'.join((_broker_url, _broker_port))

_broker_auth_sasl_plain = {
    'security_protocol': 'SASL_PLAINTEXT',
    'sasl_mechanism': 'PLAIN',
    'sasl_plain_username': os.environ.get('BROKER_USERNAME'),
    'sasl_plain_password': os.environ.get('BROKER_PASSWORD')
}

_broker_auth_ssl = {
    'security_protocol': 'SSL',
    'ssl_cafile': os.environ.get('BROKER_CA_CERT'),
    'ssl_certfile': os.environ.get('BROKER_SERVICE_CERT'),
    'ssl_keyfile': os.environ.get('BROKER_SERVICE_KEY')
}

_brokers = {
    'kafka': Producer
}

_broker_auth = {
    'sasl_plain': _broker_auth_sasl_plain,
    'ssl': _broker_auth_ssl,
    'no_auth': {'security_protocol': 'PLAINTEXT'}
}

PRODUCER = _brokers[_broker_settings['type']](
    bootstrap_servers=_broker_uri,
    **_broker_auth[_broker_settings['auth']]
)


def collect_produce_service_run(
        url: str,
        producer: Producer,
        topic: str,
        sleep_time: int,
        pattern: Optional[str] = None,
        cycles: Optional[int] = None
) -> None:
    """Service runner for web monitoring and posting to Kafka broker

    Args:
        url: url of monitored web-site
        producer: Kafka producer
        topic: Kafka topic this service will post to
        sleep_time: number of seconds to wait between metric collection
        pattern: optional regexp-like string to look at monitored web-site
        cycles: number of iterations to run the service. Runs infinitely if None

    Returns:
        None, runs until interrupted by user or iterated "iterations" times

    """
    log = logging.getLogger('WebMetricProducerService')
    log.info('Starting Website metric collection and publishing service.')
    with producer:
        counter = 0
        def proceed(): return counter < cycles if cycles else True
        while True:
            result = get_metrics(url, pattern)
            producer.send(topic, value=result)
            counter += 1
            if not proceed():
                break
            time.sleep(sleep_time)


if __name__ == '__main__':
    cmd_args = argparse.ArgumentParser()

    cmd_args.add_argument(
        '--url',
        dest='url',
        help='url to collect web metrics from, no quotes. Defaults to specified in service.yaml',
        type=str
    )
    cmd_args.add_argument(
        '--topic',
        dest='topic',
        help=f'topic name to publish, no quotes. Defaults to {TOPIC}',
        type=str
    )
    cmd_args.add_argument(
        '--cycles',
        dest='cycles',
        help='number of cycles to run, infinite if not specified',
        type=int
    )
    cmd_args.add_argument(
        '--pattern',
        dest='pattern',
        help='regexp to look at website. Defaults to one specified in service.yaml settings',
        type=str
    )
    cmd_args.add_argument(
        '--sleep',
        dest='sleep',
        help='seconds to wait between broker polling, defaults to service.yaml settings',
        type=int
    )
    args = cmd_args.parse_args()

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s | %(name)s >>> %(message)s',
        datefmt='%d-%b-%Y %H:%M:%S'
    )
    collect_produce_service_run(
        args.url if args.url else TARGET_URL,
        PRODUCER,
        args.topic if args.topic else TOPIC,
        args.sleep if args.sleep else SLEEP_BETWEEN_REQUESTS,
        pattern=args.pattern if args.pattern else TARGET_PATTERN,
        cycles=args.cycles if args.cycles else None
    )
