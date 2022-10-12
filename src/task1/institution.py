from typing import List
from abc import ABC, abstractmethod
from datetime import datetime

class Room(ABC):
    """Abstract interface for a Room"""

    def __init__(self, capacity: int, number: int, has_ac: bool, activites = []):
        self.capacity = capacity
        self.number = number
        self.has_ac = has_ac
        self.activites = activites

    def assign_activity(self, time_from, time_to, n_people):
        today = calculate_today_stamp()
        lower_limit = today + 8 * 3600
        upper_limit = today + 21 * 3600
        
        # print(datetime.fromtimestamp(today))
        # print(datetime.fromtimestamp(time_from))
        # print(datetime.fromtimestamp(time_to))
        # print(datetime.fromtimestamp(lower_limit))
        # print(datetime.fromtimestamp(upper_limit))
        if time_from < lower_limit or time_from > upper_limit:
            print("You should enter time between 8 to 21")
        elif self.capacity < n_people:
            print(f"Room number {self.number} can't fit for {n_people} people, max capacity is {self.capacity}")
        elif time_from > time_to:
            print("Wrong time format")
        
        else:
            time_from = datetime.fromtimestamp(time_from).hour
            time_to = datetime.fromtimestamp(time_to).hour
            if self.check_available(time_from, time_to):
                print("Room is not available in this time interval")
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

    def __init__(self, name: str, classroms = None, auditorium = None):
        self.name = name
        self.classroms = set()
        self.auditorium = set()

    # telling Python how to compare objects
    def __eq__(self, other):
        return self.number == other.number

    def add(self, new_room):
        if isinstance(new_room, Klassroom):
            # add it to the object of the classrom
            self.classroms.add(new_room)
            print("Classrom added successfuly")

        elif isinstance(c, LectureAuditorium):
            # add it to the object of the auditoriums
            self.auditorium.add(new_room)
            print("Auditorium added successfuly")

        else:
            print("Wrong Type")
        
    def remove(self, number, room_type):
        # Not Done Yet!!
        if Klassroom.__name__ == room_type:
            if number in self.get_classroms_numbers():
                # Remove it
                other = Klassroom(None, number, False, [])
                self.classroms.remove(other)
            else:
                print("Room does not exist")
        elif isinstance(room_type, LectureAuditorium):
            if number in auditoriums.get_audit_numbers():
                # Remove it         
                pass
            else:
                print("Room does not exist")
        else:
            print("Wrong Type")

    # @property
    # def get_classroms(self):
    #     return self.classroms

    # @property
    # def get_audits(self):
    #     return self.auditoriums

    def get_all_classroms(self):
        return '\n'.join([str(room) for room in self.classroms])
    
    def get_all_audits(self):
        return '\n'.join([str(room) for room in self.auditoriums])

    def get_all_rooms(self):
        return get_all_classroms() + '\n' + get_all_audits()

    def get_classroms_numbers(self):
        return set([number for number in self.classroms])

    def get_audit_numbers(self):
        return set([number for number in self.auditoriums.number])

    def saveToFile(self, file_name):
        """Dump all the object data in .txt file."""
        pass
    
    def restoreFromFile(self):
        """restore the object data from a .txt file."""
        pass


class Klassroom(Room):
    
    def __init__(self, capacity: int, number: int, has_ac: bool, activites = []):
        Room.__init__(self, capacity, number, has_ac, activites)

class LectureAuditorium(Room):
    
    def __init__(self, capacity: int, number: int, has_ac: bool, activites = []):
        Room.__init__(self, capacity, number, has_ac, activites)


def calculate_today_stamp():
    return datetime.now().timestamp() - (datetime.now().timestamp() % 86400)

def convert_time(hour_from, minute_from, hour_to, minute_to):

    # datetime.now().timestamp() ==> timestamp of today
    # datetime.now().timestamp() % 86400 ==> remove days
    # we do this to eliminate hours to reset to start of the current day
 
    today_stamp = calculate_today_stamp()
    time_from = today_stamp + (hour_from * 3600) + minute_from * 60
    time_to = today_stamp + (hour_to * 3600) + minute_to * 60

    return time_from, time_to


if __name__ == "__main__":
    # just for testing
    c = Klassroom(19, 1, True)
    hour_from, minute_from, hour_to, minute_to = 8, 22, 13, 51
    time_from, time_to = convert_time(hour_from, minute_from, hour_to, minute_to)
    c.assign_activity(time_from, time_to, 5)
    c.assign_activity(time_from, time_to, 5)
    print(c.activites)

    # c.assign_activity(10, 12, 5)
    # c.assign_activity(12, 11, 5)
    # c.assign_activity(10, 13, 5)
    # c.assign_activity(14, 21, 5)
    # c.assign_activity(21, 22, 5)
    # print(c.activites)
    # e = EdInstitution("Inno")
    # e.add((c))
    # # print(c in e.get_classroms)
    # e.remove(c.number, type(c).__name__)
    # print(c in e.get_classroms)
