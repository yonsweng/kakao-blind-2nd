class Truck:
    def __init__(self, truck, max_loaded_bikes, map_size):
        '''
        :param truck = {"id": int, "location_id": int, "loaded_bikes_count": int}

        self.status:
            ('STOPPED', )
            ('TO_LOAD', loading_location, putting_location, n_bikes)
            ('LOADING', putting_location, n_bikes)
            ('TO_PUT' , putting_location, n_bikes)
            ('PUTTING', n_bikes)
        '''
        self.id = truck['id']
        self.location = truck['location_id']
        self.loaded_bikes = truck['loaded_bikes_count']
        self.max_loaded_bikes = max_loaded_bikes
        self.map_size = map_size
        self.status = ('STOPPED', )

    def set_plan(self, loading_location, putting_location, n_bikes, locations):
        if n_bikes == 0:
            self.status = ('STOPPED', )
        elif loading_location == self.location:
            if locations[loading_location]['located_bikes_count'] > 0:
                self.status = ('LOADING', loading_location, putting_location, n_bikes)
        else:
            self.status = ('TO_LOAD', loading_location, putting_location, n_bikes)

    def get_move_command(self):
        destination = self.status[1]

        here_row = self.map_size - self.location % self.map_size - 1
        here_col = self.location // self.map_size
        dest_row = self.map_size - destination % self.map_size - 1
        dest_col = destination // self.map_size

        if here_col == dest_col:
            if here_row > dest_row:
                return 1
            else:
                return 3
        else:
            if here_col < dest_col:
                return 2
            else:
                return 4

    def get_command(self):
        if self.status[0] == 'STOPPED':
            return 0
        elif self.status[0] == 'TO_LOAD':
            return self.get_move_command()
        elif self.status[0] == 'LOADING':
            return 5
        elif self.status[0] == 'TO_PUT':
            return self.get_move_command()
        else:  # PUTTING
            return 6

    def execute(self, command, locations):
        if 1 <= command and command <= 4:
            if command == 1:    # GO UP
                if (self.location + 1) % self.map_size != 0:
                    self.location += 1
            elif command == 2:  # GO RIGHT
                if self.location // self.map_size + 1 < self.map_size:
                    self.location += self.map_size
            elif command == 3:  # GO DOWN
                if self.location % self.map_size != 0:
                    self.location -= 1
            else:  # command == 4, GO LEFT
                if self.location >= self.map_size:
                    self.location -= self.map_size

            if self.location == self.status[1]:
                if self.status[0] == 'TO_LOAD':
                    self.status = ('LOADING', self.status[2], self.status[3])
                else:  # TO_PUT
                    self.status = ('PUTTING', self.status[2])
        elif command == 5:  # LOAD
            location = locations[self.location]
            if location['located_bikes_count'] > 0:
                location['located_bikes_count'] -= 1
                self.loaded_bikes += 1

            # if no more bikes to load
            if location['located_bikes_count'] == 0 or \
                    self.loaded_bikes == self.status[2]:
                if self.location == self.status[1]:
                    self.status = ('PUTTING', self.status[1], self.loaded_bikes)
                else:
                    self.status = ('TO_PUT', self.status[1], self.loaded_bikes)
            else:
                self.status = ('LOADING', self.status[1], self.status[2] - 1)
        elif command == 6:  # PUT
            location = locations[self.location]
            if self.loaded_bikes > 0:
                self.loaded_bikes -= 1
                location['located_bikes_count'] += 1

            # if no more bikes to load
            if self.loaded_bikes == 0:
                self.status = ('STOPPED', )
            else:
                self.status = ('PUTTING', self.status[1] - 1)
