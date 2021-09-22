from logger import set_logger
from calls import *
from Truck import Truck


def locations_having_many(locations, N_TRUCKS):
    sorted_locations = sorted(locations, key=lambda x: -x['located_bikes_count'])
    return [location['id'] for location in sorted_locations[:N_TRUCKS]]


def locations_having_few(locations, N_TRUCKS):
    sorted_locations = sorted(locations, key=lambda x: x['located_bikes_count'])
    return [location['id'] for location in sorted_locations[:N_TRUCKS]]


def manhattan_distance(a, b, map_size):
    a_row, a_col = map_size - a % map_size - 1, a // map_size
    b_row, b_col = map_size - b % map_size - 1, b // map_size
    return abs(a_row - b_row) + abs(a_col - b_col)


def sort_loading_candidates(loading_candidates, putting_candidates, map_size):
    '''
    Sort by distance to putting_candidates
    '''
    for i, putting_location in enumerate(putting_candidates):
        for j, loading_location in enumerate(loading_candidates[i:], i):
            if manhattan_distance(loading_location, putting_location, map_size) \
                    < manhattan_distance(loading_candidates[i], putting_location, map_size):
                loading_candidates[i], loading_candidates[j] = loading_location, loading_candidates[i]


def calc_avg_bikes(locations):
    sum_bikes = 0
    for location in locations:
        sum_bikes += location['located_bikes_count']
    return sum_bikes / len(locations)


def select_loading_location(locations, truck_location, putting_location, map_size):
    a_row, a_col = map_size - truck_location % map_size - 1, truck_location // map_size
    b_row, b_col = map_size - putting_location % map_size - 1, putting_location // map_size

    max_bikes, max_location = -1, truck_location
    for row in range(min(a_row, b_row), max(a_row, b_row) + 1):
        for col in range(min(a_col, b_col), max(a_col, b_col) + 1):
            location_id = col * map_size + map_size - row - 1
            located_bikes_count = locations[location_id]['located_bikes_count']
            if located_bikes_count > max_bikes:
                max_bikes = located_bikes_count
                max_location = location_id
    return max_location


def load_offset(problem):
    return


def determine_commands(locations, offset, trucks, N_TRUCKS, map_size):
    putting_candidates = locations_having_few(locations, N_TRUCKS)

    loading_candidates = locations_having_many(locations, N_TRUCKS)
    sort_loading_candidates(loading_candidates, putting_candidates, map_size)

    avg_bikes = calc_avg_bikes(locations)

    for loading_location, putting_location in zip(loading_candidates, putting_candidates):
        # select the nearest truck
        min_distance, nearest_truck_id = 999999999, None
        for truck in trucks:
            if truck.status[0] == 'STOPPED':
                distance = manhattan_distance(truck.location, loading_location, map_size)
                if distance < min_distance:
                    min_distance = distance
                    nearest_truck_id = truck.id
        if nearest_truck_id is not None:
            # select the location having max bikes on the way
            # loading_location = select_loading_location(locations, truck.location, putting_location, map_size)

            n_putting_locations_bikes = locations[putting_location]['located_bikes_count']
            n_loading_bikes = max(0, min(truck.max_loaded_bikes, round(avg_bikes) - n_putting_locations_bikes))
            trucks[nearest_truck_id].set_plan(loading_location, putting_location, n_loading_bikes, locations)

    return [truck.get_command() for truck in trucks]


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

    trucks = get_trucks()  # [{"id": 0, "location_id": 0, "loaded_bikes_count": 0}, ...]
    trucks = [Truck(truck, MAX_LOADED_BIKES, MAP_SIZE) for truck in trucks]

    offset = load_offset(problem)

    for time in range(720):
        locations = get_locations()  # [{"id": 0, "located_bikes_count": 3}, ...]

        commands_lists = [[] for _ in range(N_TRUCKS)]

        for _ in range(COMMANDS_PER_MIN):
            commands = determine_commands(locations, offset, trucks, N_TRUCKS, MAP_SIZE)
            for truck, command, commands_list in zip(trucks, commands, commands_lists):
                commands_list.append(command)
                truck.execute(command, locations)

        response = simulate(commands_lists)

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
