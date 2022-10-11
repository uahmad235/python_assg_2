from typing import List
from abc import ABC, abstractmethod
from datetime import datetime


class Room(ABC):
    """Abstract interface for a Room"""

    def __init__(self, capacity: int, number: int, aircondition: bool, activites = []):
        self.capacity = capacity
        self.number = number
        self.aircondition = aircondition
        self.activites = activites

    def assign_activity(self, time_from, time_to, n_people):
        if time_from < 8 or time_to > 21:
            print("You should enter time between 8 to 21")
            return False
        elif self.capacity < n_people:
            print(f"Room number {self.number} can't fit for {n_people} people, max capacity is {self.capacity}")
            return False
        elif time_from > time_to:
            print("Wrong time format")
            return False
        else:
            if self.check_available(time_from, time_to):
                print("Room is not available in this time interval")
                return False
            else:
                self.activites.append((time_from, time_to))
                print("Activity has assigned successfuly")
                return True

    def check_available(self, time_from, time_to):
        for interval in self.activites:
            if time_from >= interval[1] or time_to <= interval[0]:
                continue
            if time_from >= interval[0] and time_from < interval[1]:
                return True
            elif time_to > interval[0] and time_to <= interval[1]:
                return True
            else:
                return False


class EdInstitution:

    def __init__(self, name: str, classroms = set(), auditorium = set()):
        self.name = name
        self.classroms = classroms
        self.auditorium = auditorium


    def add(self, new_room):
        tp = type(new_room).__name__
        if tp == "klassroom":
            # add it to the object of the classrom
            pass
        elif tp == "LectureAuditorium":
            # add it to the object of the auditoriums
            pass
        else:
            return "Wrong Type"
        
    def remove(self):
        number = room.number
        tp = type(new_room).__name__
        if tp ==  "klassroom":
            if number in classroms.get_classroms_numbers():
                # Remove it
                pass
            else:
                return "Room does not exist"
        elif tp ==  "LectureAuditorium":
            if number in auditoriums.get_audit_numbers():
                # Remove it         
                pass
            else:
                return "Room does not exist"
        else:
            return "Wrong Type"

    def get_all_classroms(self):
        return '\n'.join([str(room) for room in self.classroms])
    
    def get_all_audits(self):
        return '\n'.join([str(room) for room in self.auditoriums])

    def get_all_rooms(self):
        return get_all_classroms() + '\n' + get_all_audits()

    def get_classroms_numbers(self):
        return set([number for number in self.classroms.number])

    def get_audit_numbers(self):
        return set([number for number in self.auditoriums.number])

    def saveToFile(self, file_name):
        """Dump all the object data in .txt file."""
        pass
    
    def restoreFromFile(self):
        """restore the object data from a .txt file."""
        pass



class Klassroom(Room):
    pass


class LectureAuditorium(Room):
    pass




if __name__ == "__main__":
    # just for testing
    c = Klassroom(19, 1, True)
    c.assign_activity(8, 10, 5)
    print(c.activites)

    c.assign_activity(10, 12, 5)
    c.assign_activity(12, 11, 5)
    c.assign_activity(10, 13, 5)
    c.assign_activity(14, 21, 5)
    c.assign_activity(21, 22, 5)
    print(c.activites)