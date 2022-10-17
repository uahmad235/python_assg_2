import shelve
from room import Klassroom, LectureAuditorium


class EdInstitution:

    def __init__(self, name, classrooms = None, auditoriums = None):
        self.name = name
        self.classrooms = classrooms
        self.auditoriums = auditoriums

    # Comparing Objects
    def __eq__(self, other):
        return self.number == other.number

    def __str__(self):
        return f'''{self.name} Institution
        Number of classrooms: {len(self.classrooms) if self.classrooms else 0}
        Number of Auditoriums: {len(self.auditoriums) if self.auditoriums else 0}
        Status for Today (Now): {self.overall_availability()[0]} avaialbe classrooms and {self.overall_availability()[1]} available auditoriums
        '''

    def add(self, new_room):
        """
        Method to add new room the institution
        Parameters:
            new_room: the information of the new classroom / auditorium
        """
        if isinstance(new_room, Klassroom):
            # add it to the object of the classrom
            self.classrooms.add(new_room)
            print("Classrom added successfuly")

        elif isinstance(new_room, LectureAuditorium):
            # add it to the object of the auditoriums
            self.auditoriums.add(new_room)
            print("Auditorium added successfuly")

        else:
            print("Wrong Type")
        
    def remove(self, number, room_type):
        """
        Method to remove room from the institution
        Parameters:
            number: number of room to be removed from classroom / auditorium
            room_type: type of the room (classroom / auditorium)
        """
        if Klassroom.__name__ == room_type:
            if number in self.get_classrooms_numbers():
                for room in self.classrooms:
                    if room.number == number:
                        self.classrooms.remove(room)
            else:
                print("Room does not exist")
        
        if LectureAuditorium.__name__ == room_type:
            if number in self.get_audits_numbers():
                for room in self.auditoriums:
                    if room.number == number:
                        self.auditoriums.remove(room)
            else:
                print("Room does not exist")
        else:
            print("Wrong Type")

    def get_classrooms_numbers(self):
        """
        Method to return all classrooms numbers
        """
        return [room.number for room in self.classrooms]

    def get_audits_numbers(self):
        """
        Method to return all auditoriums numbers
        """
        return [room.number for room in self.auditoriums]

    def saveToFile(self, file_name):
        """Dump all the object data in shelve files."""
        db = shelve.open(file_name)
        db[self.name] = (self.name, self.classrooms, self.auditoriums)
        db.close() 

    def restoreFromFile(self, file_name):
        """restore the object data from shelve files.."""
        with shelve.open(file_name) as db:
            self.name, self.classrooms, self.auditoriums = db[self.name]
        
    def overall_availability(self):
        """
        Method to check the availability of all rooms in the institutions
        Return: number of available classrooms and number of available auditoriums
        """
        available_classrooms, available_auditoriums = 0, 0

        for classroom in self.classrooms:
            if classroom.available_today():
                available_classrooms += 1
        
        for audit in self.auditoriums:
            if audit.available_today():
                available_auditoriums += 1
        
        return available_classrooms, available_auditoriums