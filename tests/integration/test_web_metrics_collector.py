import ipaddress

import pytest
from src.metrics_collector import get_metrics, SERVICE_NAME
from datetime import timedelta, datetime


ALWAYS_AVAILABLE_URL = 'https://www.google.com'
MAXIMUM_ACCEPTABLE_RESP_TIME = 2000
STATUS_CODE_200 = 200
RE_PATTERN_VALID = 'Google '
RE_PATTERN_INVALID = 'I find your lack of faith disturbing'


@pytest.mark.integration
@pytest.mark.slow
def test_behavior_with_invalid_http_response():
    result = get_metrics('https://www.monedo.jpy/')
    try:
        datetime.strptime(result['request_timestamp'], '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        pytest.fail(f"{result['request_timestamp']} has wrong format {e.args}")
    result.pop('request_timestamp')
    assert result == {
        'url': None,
        'ip_address': None,
        'resp_time': None,
        'resp_status_code': 404,
        'pattern_found': None,
        'service_name': SERVICE_NAME
    }


@pytest.mark.integration
@pytest.mark.slow
def test_behavior_with_valid_http_response_and_no_pattern():
    # Due to datetime.utcnow() this test may fail during manual debug!
    result = get_metrics(ALWAYS_AVAILABLE_URL)
    max_timespan = timedelta(milliseconds=MAXIMUM_ACCEPTABLE_RESP_TIME)
    try:
        time = datetime.strptime(result['request_timestamp'], '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        pytest.fail(f"{result['request_timestamp']} has wrong format {e.args}")
    msg = f'Response to {ALWAYS_AVAILABLE_URL} either unsuccessful or took more than {str(max_timespan)}'
    assert max_timespan > datetime.utcnow() - time > timedelta(milliseconds=0), msg
    assert result['url'] == ALWAYS_AVAILABLE_URL
    msg = f'IP address seems have invalid format. Got: {result["url"]}'
    assert ipaddress.ip_address(result['ip_address']), msg
    try:
        t = datetime.strptime(result['resp_time'], '%H:%M:%S.%f')
        time = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
    except ValueError as e:
        pytest.fail(f"{result['request_timestamp']} has wrong format: {e.args}")
    msg = f'Elapsed argument for {ALWAYS_AVAILABLE_URL} took longer than {str(max_timespan)}'
    assert time < max_timespan, msg
    assert result['resp_status_code'] == 200
    assert result['pattern_found'] is None
    assert result['service_name'] is SERVICE_NAME


@pytest.mark.integration
@pytest.mark.slow
def test_behavior_with_valid_http_response_and_valid_pattern():
    result = get_metrics(ALWAYS_AVAILABLE_URL, RE_PATTERN_VALID)
    assert result['pattern_found'] is True


@pytest.mark.integration
@pytest.mark.slow
def test_behavior_with_valid_http_response_and_invalid_pattern():
    result = get_metrics(ALWAYS_AVAILABLE_URL, RE_PATTERN_INVALID)
    assert result['pattern_found'] is False
