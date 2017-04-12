class Room(object):
        """Room class describes the characteristics of each
        instance of a room created
        """
        def __init__(self, room_type = "", room_name = ""):
                self.room_name = room_name
                self.room_type = room_type
                self.occupants = []
                self.all_rooms = []

        def create_room(self, room_type, room_name):
                self.room_type = room_type
                self.room_name = room_name
                self.occupants = []
                self.all_rooms.append(self)
                return self


class OfficeSpace(Room):
        """This class defines an instance of each Office
        and inherits from Room class
        """
        def __init__(self, room_type = "", room_name = "" ):
                super(OfficeSpace, self).__init__(room_type, room_name)
                self.room_type = "OFFICE"
                self.room_name = room_name
                self.occupants = []
                                
                
        def create_room(self, room_type, room_name):
                self.room_type = room_type
                self.room_name = room_name
                self.all_rooms.append(self)
                self.capacity = 6
                self.occupants = []
                return self
        
class LivingSpace(Room):
        """This class defines an instance of each Livingspace
        and inherits from Room class
        """
        def __init__(self,room_type = "", room_name = ""):
                super(LivingSpace, self).__init__(room_name)
                self.room_type = "LIVING SPACE"
                self.room_name = room_name
                self.occupants = []

        def create_room(self, room_type, room_name):
                self.room_type = room_type
                self.room_name = room_name
                self.capacity = 4
                self.occupants = []
                self.all_rooms.append(self)
                return self


