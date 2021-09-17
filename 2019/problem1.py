import requests
import json


def random_starts_ids(calls, k, this_floor):
    ''' calls에서 k명의 id를 list로 반환 '''
    ids = []
    not_appended = []
    for call in calls:
        if call['start'] == this_floor:
            ids.append(call['id'])
            k -= 1
            if k == 0:
                break
        else:
            not_appended.append(call)
    return ids, not_appended


def random_ends_ids(calls, k, this_floor):
    ''' calls에서 k명의 id를 list로 반환 '''
    ids = []
    not_appended = []
    for call in calls:
        if call['end'] == this_floor:
            ids.append(call['id'])
            k -= 1
            if k == 0:
                break
        else:
            not_appended.append(call)
    return ids, not_appended


def are_starts_this_floor(calls, this_floor):
    for call in calls:
        if call['start'] == this_floor:
            return True
    return False


def are_ends_this_floor(calls, this_floor):
    for call in calls:
        if call['end'] == this_floor:
            return True
    return False


def are_starts_more_above(calls, this_floor):
    cnt = 0
    for call in calls:
        if call['start'] > this_floor:
            cnt += 1
    return True if cnt * 2 > len(calls) else False


def are_ends_more_above(calls, this_floor):
    cnt = 0
    for call in calls:
        if call['end'] > this_floor:
            cnt += 1
    return True if cnt * 2 > len(calls) else False


N_ELEVATORS = 4
problem_id = 2
if problem_id == 1:
    top_floor = 5
else:
    top_floor = 25

r = requests.post(f'http://localhost:8000/start/tester/{problem_id}/{N_ELEVATORS}')
if r.status_code == 200:
    token = r.json()['token']

while True:
    r = requests.get('http://localhost:8000/oncalls', headers={'X-Auth-Token': token})
    oncalls = r.json()

    if oncalls['is_end']:
        break

    commands = [{'elevator_id': i} for i in range(N_ELEVATORS)]
    action = {'commands': commands}
    calls = oncalls['calls']
    for elevator in oncalls['elevators']:
        if are_ends_this_floor(elevator['passengers'], elevator['floor']):  # 내릴 사람이 있는 경우
            if elevator['status'] == 'UPWARD' or elevator['status'] == 'DOWNWARD':
                commands[elevator['id']]['command'] = 'STOP'
            elif elevator['status'] == 'STOPPED':
                commands[elevator['id']]['command'] = 'OPEN'
            elif elevator['status'] == 'OPENED':
                commands[elevator['id']]['command'] = 'EXIT'
                commands[elevator['id']]['call_ids'], elevator['passengers'] = random_ends_ids(elevator['passengers'], len(elevator['passengers']), elevator['floor'])
        elif len(elevator['passengers']) < 8 and are_starts_this_floor(calls, elevator['floor']):  # 탈 사람이 있는 경우
            if elevator['status'] == 'UPWARD' or elevator['status'] == 'DOWNWARD':
                commands[elevator['id']]['command'] = 'STOP'
            elif elevator['status'] == 'STOPPED':
                commands[elevator['id']]['command'] = 'OPEN'
            elif elevator['status'] == 'OPENED':
                commands[elevator['id']]['command'] = 'ENTER'
                commands[elevator['id']]['call_ids'], calls = random_starts_ids(calls, 8 - len(elevator['passengers']), elevator['floor'])
        else:
            if elevator['status'] == 'UPWARD':
                if elevator['floor'] == top_floor:
                    commands[elevator['id']]['command'] = 'STOP'
                else:
                    commands[elevator['id']]['command'] = 'UP'
            elif elevator['status'] == 'DOWNWARD':
                if elevator['floor'] == 1:
                    commands[elevator['id']]['command'] = 'STOP'
                else:
                    commands[elevator['id']]['command'] = 'DOWN'
            elif elevator['status'] == 'STOPPED':
                if len(elevator['passengers']) > 0:
                    if are_ends_more_above(elevator['passengers'], elevator['floor']):
                        commands[elevator['id']]['command'] = 'UP'
                    else:
                        commands[elevator['id']]['command'] = 'DOWN'
                elif len(calls) == 0:
                    commands[elevator['id']]['command'] = 'STOP'
                elif are_starts_more_above(calls, elevator['floor']):
                    commands[elevator['id']]['command'] = 'UP'
                else:
                    commands[elevator['id']]['command'] = 'DOWN'
            elif elevator['status'] == 'OPENED':
                commands[elevator['id']]['command'] = 'CLOSE'

    r = requests.post('http://localhost:8000/action', headers={'X-Auth-Token': token}, data=json.dumps(action))
