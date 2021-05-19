import pytest

from src.service import TOPIC, AIVEN_KAFKA_PRODUCER as producer


"""This test ensure that kafka producer is properly configured
and the overall setup (including Aiven kafka broker) is working"""


@pytest.mark.smoke
def test_smoke_kafka_producer():
    with producer:
        producer._producer.config['max_block_ms'] = 3000
        producer.send(TOPIC, data)


data = {
    'request_timestamp': '2021-01-01 00:00:00',
    'url': 'https://www.monedo.com/',
    'ip_address': '104.18.91.87',
    'resp_time': '0:00:00.123456',
    'resp_status_code': 200,
    'pattern_found': True,
    'service_name': 'Web metric collection service',
    'comment': 'test'
}
