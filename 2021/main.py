from logger import set_logger
from calls import *
from Truck import Truck

UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4
LOAD = 5
PUT = 6


def calc_avg_bikes(locations):
    sum_bikes = 0
    for location in locations:
        sum_bikes += location['located_bikes_count']
    return sum_bikes / len(locations)


def get_command1(located_bikes_count, avg_bikes, loaded_bikes, MAX_LOADED_BIKES, row, col, n_cols, truck_num, curr_direction, map_size):
    if located_bikes_count > avg_bikes + 0.5 and loaded_bikes < MAX_LOADED_BIKES:
        return LOAD
    elif located_bikes_count < avg_bikes - 0.5 and loaded_bikes > 0:
        return PUT
    elif col < n_cols * truck_num:
        return RIGHT
    elif row == 0:
        return UP
    elif row == map_size - 1:
        return DOWN
    else:
        return curr_direction


def get_command2(located_bikes_count, avg_bikes, loaded_bikes, MAX_LOADED_BIKES, row, col, n_cols, truck_num, map_size):
    if located_bikes_count > avg_bikes + 0.5 and loaded_bikes < MAX_LOADED_BIKES:
        return LOAD
    elif located_bikes_count < avg_bikes - 0.5 and loaded_bikes > 0:
        return PUT
    elif col < n_cols * truck_num:
        return RIGHT
    elif row == 0 and col % n_cols == 0:
        return RIGHT
    elif col % n_cols == 0:
        return DOWN
    elif row % 2 == 0 and (col + 1) % n_cols == 0:
        return UP
    elif row % 2 == 1 and col % n_cols == 1 and row + 1 < map_size:
        return UP
    elif row % 2 == 0:
        return RIGHT
    else:
        return LEFT


def move_trucks(problem):
    LOGGING_TERM = 80
    COMMANDS_PER_MIN = 10
    MAX_LOADED_BIKES = 20
    if problem == 1:
        MAP_SIZE = 5
        N_TRUCKS = 5
    else:
        MAP_SIZE = 60
        N_TRUCKS = 10

    n_cols = MAP_SIZE // N_TRUCKS

    api_trucks = get_trucks()  # [{"id": 0, "location_id": 0, "loaded_bikes_count": 0}, ...]
    trucks = [Truck(truck, MAX_LOADED_BIKES, MAP_SIZE) for truck in api_trucks]

    for time in range(720):
        api_trucks = get_trucks()  # [{"id": 0, "location_id": 0, "loaded_bikes_count": 0}, ...]
        locations = get_locations()  # [{"id": 0, "located_bikes_count": 3}, ...]

        for api_truck, truck in zip(api_trucks, trucks):
            truck.init(api_truck)

        commands = [[] for _ in range(N_TRUCKS)]

        avg_bikes = calc_avg_bikes(locations)

        for _ in range(COMMANDS_PER_MIN):
            for truck_num, truck in enumerate(trucks):
                location = locations[truck.location]
                location_id = location['id']
                located_bikes_count = location['located_bikes_count']
                row, col = location_id % MAP_SIZE, location_id // MAP_SIZE
                loaded_bikes = truck.loaded_bikes

                if problem == 1:
                    command = get_command1(located_bikes_count, avg_bikes, loaded_bikes, MAX_LOADED_BIKES, row, col, n_cols, truck_num, truck.curr_direction, MAP_SIZE)
                else:
                    command = get_command2(located_bikes_count, avg_bikes, loaded_bikes, MAX_LOADED_BIKES, row, col, n_cols, truck_num, MAP_SIZE)

                commands[truck_num].append(command)
                truck.go(command, location)

        response = simulate(commands)

        # log by each 80 mins
        if (time + 1) % LOGGING_TERM == 0:
            logger.info(response)


def main():
    PROBLEM = 1
    logger.info(f'problem {PROBLEM} start!')

    start(PROBLEM)
    move_trucks(PROBLEM)

    score = get_score()
    logger.info(f'problem {PROBLEM} score: {score}')


if __name__ == '__main__':
    logger = set_logger()
    main()
