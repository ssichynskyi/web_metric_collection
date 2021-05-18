import logging
import os
import time

from typing import Optional
from src.metrics_collector import get_metrics
from src.producer import Producer
from utils.env_config import config


TOPIC = 'website-metrics'

_sleep_after_request = config['Monitored web sites']['monedo']['request sleep']
_target_url = config['Monitored web sites']['monedo']['url']
_target_pattern = config['Monitored web sites']['monedo']['expected pattern']
_kafka_url = config['Metrics endpoint']['Aiven']['Kafka']['host']
_kafka_port = str(config['Metrics endpoint']['Aiven']['Kafka']['port'])
_kafka_uri = ':'.join((_kafka_url, _kafka_port))
_ca_path = os.environ['CA-CERT']
_cert_path = os.environ['SERVICE_CERT']
_key_path = os.environ['SERVICE-KEY']
aiven_kafka_producer = Producer(_kafka_uri, _ca_path, _cert_path, _key_path)


def main(
        url: str,
        producer: Producer,
        topic: str,
        sleep_time: int,
        pattern: Optional[str] = None
) -> None:
    """Service runner for web monitoring and posting to Kafka broker

    Args:
        url: url of monitored web-site
        producer: Kafka producer
        topic: Kafka topic this service will post to
        sleep_time: number of seconds to wait between metric collection
        pattern: optional regexp-like string to look at monitored web-site

    Returns:
        None, runs until interrupted by user

    """
    log = logging.getLogger('WebMetricProducerService')
    log.info('Starting Website metric collection and publishing service.')
    with producer:
        while True:
            result = get_metrics(url, pattern)
            producer.send(topic, value=result)
            time.sleep(sleep_time)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s | %(name)s >>> %(message)s',
        datefmt='%d-%b-%Y %H:%M:%S'
    )
    # ToDo: pass topic as a sys arg
    main(_target_url, aiven_kafka_producer, TOPIC, _sleep_after_request, _target_pattern)
