import pytest

from src.metrics_collector import parse_response
from tests.mocks.web_response_mock import POSITIVE_HTTP_RESP, TIMESPAN, STATUS_CODE_200


RE_PATTERN_VALID = '<h1.*?>Monedo is where the best finance and tech brains come together</h1>'
RE_PATTERN_INVALID = '<h1.*?>I find your lack of faith disturbing</h1>'


@pytest.mark.unit
def test_parse_response_no_re_pattern():
    result = parse_response(POSITIVE_HTTP_RESP)
    assert result == ('0.0.0.0', TIMESPAN, STATUS_CODE_200, None)


@pytest.mark.unit
def test_parse_response_with_matching_re_pattern():
    result = parse_response(POSITIVE_HTTP_RESP, RE_PATTERN_VALID)
    assert result == ('0.0.0.0', TIMESPAN, STATUS_CODE_200, True)


@pytest.mark.unit
def test_parse_response_with_not_matching_re_pattern():
    result = parse_response(POSITIVE_HTTP_RESP, RE_PATTERN_INVALID)
    assert result == ('0.0.0.0', TIMESPAN, STATUS_CODE_200, False)
