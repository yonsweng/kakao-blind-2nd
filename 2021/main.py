from calls import *


def move_trucks():
    for time in range(720):
        locations = get_locations()  # [{"id": 0, "located_bikes_count": 3}, ...]
        trucks = get_trucks()  # [{"id": 0, "location_id": 0, "loaded_bikes_count": 0}, ...]

        commands = [[] for _ in range(N_TRUCKS)]
        simulate(commands)


def main():
    start(PROBLEM)
    move_trucks()
    print(get_score())


if __name__ == '__main__':
    PROBLEM = 1
    if PROBLEM == 1:
        SIZE = 5
        N_TRUCKS = 5
    else:
        SIZE = 60
        N_TRUCKS = 10

    main()
