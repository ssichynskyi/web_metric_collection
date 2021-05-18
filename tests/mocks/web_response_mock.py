from datetime import timedelta
from unittest.mock import Mock


TIMESPAN = timedelta(milliseconds=200)
STATUS_CODE_200 = 200


POSITIVE_HTTP_RESP = Mock()
"""Mocks positive http response as provided by requests lib"""
POSITIVE_HTTP_RESP.raw._fp.fp.raw._sock.getpeername.return_value = ('0.0.0.0', 443)
POSITIVE_HTTP_RESP.elapsed = TIMESPAN
POSITIVE_HTTP_RESP.status_code = STATUS_CODE_200
POSITIVE_HTTP_RESP.text = '<h1>Monedo is where the best finance and tech brains come together</h1>'
