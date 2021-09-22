import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json

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


def start(problem):
    global auth_key
    session = requests.Session()
    try:
        r = session.post(
            'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users/start',
            headers={'X-Auth-Token': '30892db98d188b94203da89d0993418f'},
            data={'problem': problem},
        )
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    auth_key = r.json()['auth_key']


def get_locations():
    global auth_key
    session = requests.Session()
    try:
        r = session.get(
            'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users/locations',
            headers={'Authorization': auth_key},
        )
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return r.json()['locations']  # [{"id": 0, "located_bikes_count": 3}, ...]


def get_trucks():
    global auth_key
    session = requests.Session()
    try:
        r = session.get(
            'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users/trucks',
            headers={'Authorization': auth_key},
        )
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return r.json()['trucks']  # [{"id": 0, "location_id": 0, "loaded_bikes_count": 0}, ...]


def simulate(commands):
    '''
    commands: [[0, 1, 2, 3, 4, 5, 6, 0, 1, 2], ...]
    -> commands = [{'truck_id': 0, 'command': [0, 1, 2, 3, 4, 5, 6, 0, 1, 2]}, ...]
    '''
    global auth_key
    commands = [{'truck_id': truck_id, 'command': command}
                for truck_id, command in enumerate(commands)]
    session = requests.Session()
    try:
        r = session.put(
            'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users/simulate',
            headers={'Authorization': auth_key},
            data=json.dumps({'commands': commands}),
        )
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return r.json()


def get_score():
    global auth_key
    session = requests.Session()
    try:
        r = session.get(
            'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users/score',
            headers={'Authorization': auth_key},
        )
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return r.json()['score']
