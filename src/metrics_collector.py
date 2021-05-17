import logging
import re
import requests

from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple

log = logging.getLogger(__name__)
SERVICE_NAME = 'Web metric collection service'


def get_metrics(url: str, re_pattern: Optional[str] = None) -> Dict:
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
        log.info(f'Sending get request to: {url}')
        resp = requests.get(url, headers=headers, stream=True)
    except requests.exceptions.ConnectionError:
        result = {
            'request_timestamp': None,
            'url': None,
            'ip_address': None,
            'resp_time': None,
            'resp_status_code': 404,
            'pattern_found': False if re_pattern else None,
            'service_name': SERVICE_NAME
        }
        return result
    rest = parse_response(resp, re_pattern)
    log.info(f'Received response from: {url}. Within: {rest[1]} with status: {rest[2]}')
    result = {
        'request_timestamp': request_time.strftime('%Y-%m-%d %H:%M:%S'),
        'url': url,
        'ip_address': rest[0],
        'resp_time': str(rest[1]),
        'resp_status_code': rest[2],
        'pattern_found': rest[3],
        'service_name': SERVICE_NAME
    }
    return result


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
        log.info(f'Pattern {re_pattern} found in response!')
    else:
        pattern_found = None
    return ip, resp_time, resp.status_code, pattern_found
