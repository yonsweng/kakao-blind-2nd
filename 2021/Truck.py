class Truck:
    def __init__(self, truck, max_loaded_bikes, map_size):
        '''
        :param truck = {"id": int, "location_id": int, "loaded_bikes_count": int}
        '''
        self.location = truck['location_id']
        self.loaded_bikes = truck['loaded_bikes_count']
        self.max_loaded_bikes = max_loaded_bikes
        self.map_size = map_size
        self.curr_direction = None

    def init(self, truck):
        self.location = truck['location_id']
        self.loaded_bikes = truck['loaded_bikes_count']

    def go(self, command, location):
        if command == 1:  # go up
            self.location = (self.location + 1) if (self.location + 1) % self.map_size != 0 else self.location
            self.curr_direction = 1
        elif command == 2:  # go right
            self.location = (self.location + self.map_size) if self.location + self.map_size < self.map_size * self.map_size else self.location
        elif command == 3:  # go down
            self.location = (self.location - 1) if self.location % self.map_size != 0 else self.location
            self.curr_direction = 3
        elif command == 4:  # go left
            self.location = (self.location - self.map_size) if self.location - self.map_size >= 0 else self.location
        elif command == 5:  # load
            if self.loaded_bikes < self.max_loaded_bikes:
                self.loaded_bikes = self.loaded_bikes + 1
                location['located_bikes_count'] = location['located_bikes_count'] - 1
        elif command == 6:  # put
            if self.loaded_bikes > 0:
                self.loaded_bikes = self.loaded_bikes - 1
                location['located_bikes_count'] = location['located_bikes_count'] + 1
