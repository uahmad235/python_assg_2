import json
from typing import List
from abc import ABC, abstractmethod
from datetime import datetime, date, time 
import sys, os

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

    def available_today(self):
        if len(self.activites) == 0:
            return True
        
        sorted_act = sorted(self.acitivites)
        for i in range(len(sorted_act) - 1):
            duration = sorted_act[i + 1][0] - sorted_act[i][1]
            duration_in_s = duration.total_seconds()
            hours = divmod(duration_in_s, 3600)[0] 
            if hours >= 1:
                return True

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
        Number of Auditoriums: {len(self.auditoriums) if self.auditoriums else 0}
        Status for Today (Now): {self.overall_availability()[0]} avaialbe classrooms and {self.overall_availability()[1]} available auditoriums
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

    def overall_availability(self):
        available_classrooms, available_auditoriums = 0, 0
        
        for classroom in (self.classrooms):
            if classroom.available_today():
                available_classrooms += 1
        
        for audit in (self.auditoriums):
            if audit.available_today():
                available_auditoriums += 1
        
        return available_classrooms, available_auditoriums


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

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    # just for testing

    # Block output at this point
    blockPrint()
    
    institutions, classrooms, auditoriums = dict(), dict(), dict()
    e1, e2 = EdInstitution("Innopolis"), EdInstitution("Kazan Federal")
    institutions[e1.name] = e1
    institutions[e2.name] = e2
    room1, audit1 = Klassroom(10, 1, True), LectureAuditorium(15, 1, False)
    room2, audit2 = Klassroom(10, 2, True), LectureAuditorium(15, 2, False)
    classrooms[1], classrooms[2] = room1, room2
    auditoriums[1], auditoriums[2] = audit1, audit2
    e1.add(room1)
    e1.add(audit1)
    e2.add(room2)
    e2.add(audit2)
    
    # Restore output here
    enablePrint()

    while True:
        
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
                    classrooms[room_number] = classroom
                    print(classroom)
                    print()
                
                elif room_type == 2:
                    print("Enter (capacity, number, air conditioner- yes/no): ")
                    capacity = int(input())
                    room_number = int(input())
                    conditioner = bool(int(input()))
                    audit = LectureAuditorium(capacity, room_number, conditioner)
                    inst.add(audit)    
                    auditoriums[room_number] = audit            
                    print(audit)
                    print()
                
                else:
                    print("Wrong Entry!")

        elif inp == 2:

            inst_name = input("Enter institution name : ")
            inst = institutions.get(inst_name, False)
            if not inst:
                print("institutions not exist\n")
            else:
                print(inst)
            
        elif inp == 3:
            print("Choose one of the following Institution:\n")
            for instituion in institutions.values():
                print(instituion.name)
            instituion = input("Enter Institution name \n")
            instituion = institutions.get(instituion, False)
            if not instituion:
                print("Wrong Name, Plase choose one from the list\n")
            else:
                available_numbers = set()
                for classroom in instituion.classrooms:
                    print(classroom)
                    available_numbers.add(classroom.number)
                classroom_number = int(input("Enter Classrom number "))
                if classroom_number not in available_numbers:
                    print("Wrong Number, Please choose number from the list above!\n")
                else:
                    choosen_room = classrooms[classroom_number]
                    time_from_h = int(input("Please enter the hour of starting "))
                    time_from_m = int(input("Please enter the minute of starting "))

                    time_to_h = int(input("Please enter the hour of ending "))
                    time_to_m = int(input("Please enter the minute of ending "))

                    number_of_people = int(input("Please enter number of attendance "))

                    time_from, time_to = convert_time(time_from_h, time_from_m, time_to_h, time_to_m)
                    choosen_room.assign_activity(time_from, time_to, number_of_people)
                    print()
                
        elif inp == 4:
            print("Choose one of the following Institution:\n")
            
            for instituion in institutions.values():
                print(instituion.name)
            instituion = input("Enter Institution name \n")
            instituion = institutions.get(instituion, False)
            if not instituion:
                print("Wrong Name, Plase choose one from the list\n")
            else:
                available_numbers = set()
                for audit in instituion.auditoriums:
                    print(audit)
                    available_numbers.add(audit.number)
                audit_number = int(input("Enter Auditoriums number "))
                if audit_number not in available_numbers:
                    print("Wrong Number, Please choose number from the list above!")
                else:
                    choosen_audit = auditoriums[audit_number]
                    time_from_h = int(input("Please enter the hour of starting"))
                    time_from_m = int(input("Please enter the minute of starting"))

                    time_to_h = int(input("Please enter the hour of ending"))
                    time_to_m = int(input("Please enter the minute of ending"))

                    number_of_people = int(input("Please enter number of attendance"))

                    time_from, time_to = convert_time(time_from_h, time_from_m, time_to_h, time_to_m)
                    choosen_audit.assign_activity(time_from, time_to, number_of_people)
                    print()     
            
        elif inp == 5:
            print("In database we have:")
            for institution in institutions:
                print(institutions[institution])
            break
            
        else:
            print("Wrong choice!")