import os
import time

from src.metrics_collector import get_metrics
from src.producer import Producer
from utils.env_config import config


def main(url, pattern, producer, sleep_time):
    while True:
        result = get_metrics(url, pattern)
        with producer:
            aiven_kafka_producer.send('website-metrics', value=result)
        time.sleep(sleep_time)


if __name__ == '__main__':
    sleep_time = config['Monitored web sites']['monedo']['request sleep']
    target_url = config['Monitored web sites']['monedo']['url']
    target_pattern = config['Monitored web sites']['monedo']['expected pattern']
    _kafka_url = config['Metrics endpoint']['Aiven']['Kafka']['host']
    _kafka_port = str(config['Metrics endpoint']['Aiven']['Kafka']['port'])
    kafka_uri = ':'.join((_kafka_url, _kafka_port))
    ca_path = os.environ['CA-CERT']
    cert_path = os.environ['SERVICE_CERT']
    key_path = os.environ['SERVICE-KEY']
    aiven_kafka_producer = Producer(kafka_uri, ca_path, cert_path, key_path)

    main(target_url, target_pattern, aiven_kafka_producer, sleep_time)
