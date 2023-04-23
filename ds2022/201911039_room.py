class Room:
    # you should initialize all the required instance variables here
    # parameters:
    #   (integer) number: room number 
    #   (integer) bed_count: number of beds in the room (you can assume it's given always >0)
    def __init__(self, number, bed_count):
        self.number = number
        self.bed_count = bed_count
        self.clients_count = 0
        self.clients = []

    # this will be called when string representation is required
    # return: (string) with the following formatting 
    #         'Room number {room number}, occupancy {currently occupied beds}/{total beds}'
    #          example return str: 'Room number 101, occupancy 2/2'
    def __str__(self):
        return(f'Room number {self.number}, occupancy {self.clients_count}/{self.bed_count}')

    # return: (integer) room number 
    def get_number(self):
        return self.number

    # return: (integer) number of beds in the room
    def get_bed_count(self):
        return self.bed_count

    # return: (integer) number of empty bed remaining in the room
    def available(self):
        return self.bed_count - self.clients_count

    # parameters:
    #   client_name: a name of client who's willing to check in to the room
    # return: (bool)
    #   True  if there was an empty bed, and the client occupies the bed
    #   False if the room was already full
    def check_in(self, client_name):
        if(self.available() > 0):
            self.clients.append(client_name)
            self.clients_count += 1
            return True
        return False

    # parameters:
    #   client_name: a name of client who's willing to check out from the room
    # return: (bool)
    #   True  if the client is actually checked in the room, and checked out successfully
    #   False if the client is nonexisting in the room
    def check_out(self, client_name):
        if(client_name in self.clients):
            self.clients.remove(client_name)
            self.clients_count -= 1
            return True
        return False

    # return: (string) 'Empty' if the room is empty, 
    #                  or a string which lists the clients in the room (separated by ', ')
    #                  -> ex: "clinet1, client2, client3"
    def get_clients(self):
        if self.clients_count == 0:
            return 'Empty'
        return ', '.join(self.clients)