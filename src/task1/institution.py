import json
from typing import List
from abc import ABC, abstractmethod
from datetime import datetime, date, time 

class Room(ABC):
    """Abstract interface for a Room"""

    def __init__(self, capacity: int, number: int, has_ac: bool, activites = []):
        self.capacity = capacity
        self.number = number
        self.has_ac = has_ac
        self.activites = activites

    def __str__(self):
        return f'''Room Type: {type(self).__name__}
        Room Number: {self.number}
        Capacity: {self.capacity}
        Air Conditioner? {"Installed" if self.has_ac else "Not Installed"}'''

    def assign_activity(self, time_from, time_to, n_people):
        
        # print(datetime.fromtimestamp(today))
        if time_from < datetime.now().replace(hour = 8, minute = 0) or time_from > datetime.now().replace(hour = 21, minute = 0):
            print("You should enter time between 8 to 21")
        elif self.capacity < n_people:
            print(f"Room number {self.number} can't fit for {n_people} people, max capacity is {self.capacity}")
        elif time_from > time_to:
            print("Wrong time format")
        
        else:
            if self.check_available(time_from, time_to):
                print("Room is not available in this time interval")
            else:
                self.activites.append((time_from, time_to))
                print("Activity has assigned successfuly")

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

    def __init__(self, name, classrooms = None, auditoriums = None):
        self.name = name
        self.classrooms = set()
        self.auditoriums = set()

    # telling Python how to compare objects
    def __eq__(self, other):
        return self.number == other.number

    def __str__(self):
        return f'''{self.name} Institution
        Number of classrooms: {len(self.classrooms) if self.classrooms else 0}
        Number of Auditoriums: {len(self.classrooms) if self.classrooms else 0}
        '''

    def add(self, new_room):
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
        # Not Done Yet!!
        if Klassroom.__name__ == room_type:
            if number in self.get_classrooms_numbers():
                # Remove it
                for room in self.classrooms:
                    if room.number == number:
                        self.classrooms.remove(room)
            else:
                print("Room does not exist")
        
        if LectureAuditorium.__name__ == room_type:
            if number in self.get_audits_numbers():
                # Remove it
                for room in self.auditoriums:
                    if room.number == number:
                        self.auditoriums.remove(room)
            else:
                print("Room does not exist")
        else:
            print("Wrong Type")

    # @property
    # def get_classrooms(self):
    #     return self.classrooms

    # @property
    # def get_audits(self):
    #     return self.auditoriums

    def get_all_classrooms(self):
        classrooms = '\n'.join([str(room.number) for room in self.classrooms])
    
    def get_all_audits(self):
        return '\n'.join([str(room) for room in self.auditoriums])

    def get_all_rooms(self):
        return self.get_all_classrooms() + '\n' + self.get_all_audits()

    def get_classrooms_numbers(self):
        return [room.number for room in self.classrooms]

    def get_audits_numbers(self):
        return [room.number for room in self.auditoriums]

    def saveToFile(self, file_name):
        """Dump all the object data in .txt file."""
        with open(file_name, 'a') as file:
            # Not implemented yet
            json.dump("Something", file)
    
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
    # the start of the current day
    return datetime.combine(date.today(), time())

def convert_time(hour_from, minute_from, hour_to, minute_to):
 
    today_date = calculate_today_stamp()
    time_from = datetime.now().replace(hour = hour_from, minute = minute_from, second = 0, microsecond = 0)
    time_to = datetime.now().replace(hour = hour_to, minute = minute_to, second = 0, microsecond = 0)

    return time_from, time_to


if __name__ == "__main__":
    # just for testing

    institutions = dict()
    e1, e2 = EdInstitution("Innopolis"), EdInstitution("Kazan Federal")
    institutions[e1.name] = e1
    institutions[e2.name] = e2

    ####### should assign activity be in Room class or in Institution class????

    # just for testing
    print("Choose one operation from below :")
    print("1 : Add classroom or Auditorium to institution")
    print("2 : Print institution summary")
    print("3 : Assign activity to classroom")
    print("4 : Assign activity to LectureAuditorium")
    print("5 : Exit program")

    inp = int(input())
    if inp == 1:
        
        inst_name = input("Enter institution name : ")
        inst = institutions.get(inst_name, False)
        if not inst:
            print("institutions not exist\n")
        else:
            room_type = int(input("Enter (classroom - 1 or Auditorium - 2): "))
            
            if room_type == 1:
                print("Enter (capacity, number, air conditioner- yes/no): ")
                capacity = int(input())
                room_number = int(input())
                conditioner = bool(int(input()))
                classroom = Klassroom(capacity, room_number, conditioner)
                inst.add(classroom)
                print(classroom)
                print()
            
            elif room_type == 2:
                print("Enter (capacity, number, air conditioner- yes/no): ")
                capacity = int(input())
                room_number = int(input())
                conditioner = bool(int(input()))
                audit = LectureAuditorium(capacity, room_number, conditioner)
                inst.add(audit)                
                print(audit)
                print()
            else:
                print("Wrong Entry!")
        
    elif inp == 2:

        inst_name = input("Enter institution name : ")
        inst = institutions.get(inst_name, False)
        if not inst:
            print("institutions not exist")
        else:
            print(inst)
        
    elif inp == 3:
        classroom_number = int(input("Enter Classrom number "))
        classrooms_numbers = []
        for instituion in institutions.values():
            classrooms_numbers.extend(instituion.get_classrooms_numbers())
        if classroom_number in classrooms_numbers:
            time_from_h = int(input("Please enter the hour of starting"))
            time_from_m = int(input("Please enter the minute of starting"))

            time_to_h = int(input("Please enter the hour of ending"))
            time_to_m = int(input("Please enter the minute of ending"))

            number_of_people = int(input("Please enter number of attendance"))

            time_from, time_to = convert_time(time_from_h, time_from_m, time_to_h, time_to_m)
            # classroom.assign_activity(time_from, time_to, number_of_people)
        
    elif inp == 4:
        audit_number = int(input("Enter Auditorium number "))
        audits_numbers = []
        for instituion in institutions.values():
            audits_numbers.extend(instituion.get_audits_numbers())
        if audit_number in audits_numbers:
            time_from_h = int(input("Please enter the hour of starting"))
            time_from_m = int(input("Please enter the minute of starting"))

            time_to_h = int(input("Please enter the hour of ending"))
            time_to_m = int(input("Please enter the minute of ending"))

            number_of_people = int(input("Please enter number of attendance"))

            time_from, time_to = convert_time(time_from_h, time_from_m, time_to_h, time_to_m)
            # audit.assign_activity(time_from, time_to, number_of_people)        
        
    elif inp == 5:
        print("In database we have:")
        for institution in institutions:
            print(institutions[institution])
        
    else:
        print("Wrong choice!")