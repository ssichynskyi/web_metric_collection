import pytest

from src.service import TOPIC, aiven_kafka_producer as producer


"""This test ensure that kafka producer is properly configured
and the overall setup (including Aiven kafka broker) is working"""


@pytest.mark.smoke
def test_smoke_kafka_producer():
    with producer:
        producer._producer.config['max_block_ms'] = 3000
        producer.send(TOPIC, {'comment': 'test'})
