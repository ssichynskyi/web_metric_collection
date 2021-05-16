from datetime import datetime, timedelta
import re
import requests
from typing import Optional, Tuple


SERVICE_NAME = 'Web metric collection service'


def get_metrics(url: str, re_pattern: Optional[str] = None) -> Tuple[
    Optional[datetime], Optional[str], Optional[str], Optional[timedelta],
    int, Optional[bool], str
]:
    """Collects metrics

    Args:
        url: url as string
        re_pattern: regexp pattern to look in http response

    Returns:
         metrics and other params as tuple

    """
    request_time = datetime.utcnow()
    headers = {'User-Agent': SERVICE_NAME}
    try:
        resp = requests.get(url, headers=headers, stream=True)
    except requests.exceptions.ConnectionError:
        return None, None, None, None, 404, False, SERVICE_NAME
    return request_time, url, *parse_response(resp, re_pattern), SERVICE_NAME


def parse_response(resp: requests.Response, re_pattern: Optional[str] = None) -> Tuple[
    str, timedelta, int, Optional[bool]
]:
    """Parses valid response

    Args:
        resp: http response as specified in requests library
        re_pattern: regexp pattern to look in http response

    Returns:
        tuple of http response params

    """
    # kinda hack to get the ip address from requests by using protected members
    ip = resp.raw._fp.fp.raw._sock.getpeername()[0]
    resp_time = resp.elapsed
    if re_pattern:
        pattern_found = True if re.findall(re_pattern, resp.text) else False
    else:
        pattern_found = None
    return ip, resp_time, resp.status_code, pattern_found
