import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from urllib.parse import urljoin

BASE_URL = ''
X_AUTH_TOKEN = ''
auth_key = None


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = requests.Session() if session is None else session
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def start(problem_num):
    global auth_key
    session = requests.Session()
    try:
        r = session.post(
            urljoin(BASE_URL, ''),
            headers={'X-Auth-Token': X_AUTH_TOKEN},
            data=json.dumps({'problem': problem_num}),
        )
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    auth_key = r.json()['auth_key']
