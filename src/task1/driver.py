
import os
import sys

from room import Klassroom, LectureAuditorium
from institution import EdInstitution
from utils import convert_time

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def print_institutions_info():
    print("we have the following instituions in the system:\n")
    for institution in institutions.keys():
        print(institution)
    print()


def print_welcome_menu():
    print("Choose one operation from below :")
    print("1 : Add classroom or Auditorium to institution")
    print("2 : Print institution summary")
    print("3 : Assign activity to classroom")
    print("4 : Assign activity to LectureAuditorium")
    print("5 : Exit program")

def get_institution(institutions):
    inst_name = input("Enter institution name : ")
    inst = institutions.get(inst_name, False)
    return inst

def print_institution_summary(institutions):
    print_institutions_info()
    inst = get_institution(institutions)
    if not inst:
        print("institutions not exist\n")
    else:
        print(inst)

def print_exit_summary(institutions):
    print("In database we have:")
    for institution in institutions:
        print(institutions[institution])

def ask_time():
    time_from_h = int(input("Please enter the hour of starting "))
    time_from_m = int(input("Please enter the minute of starting "))

    time_to_h = int(input("Please enter the hour of ending "))
    time_to_m = int(input("Please enter the minute of ending "))

    number_of_people = int(input("Please enter number of attendance "))
    return time_from_h,time_from_m,time_to_h,time_to_m,number_of_people
    

if __name__ == "__main__":
    # just for testing

    # Block output at this point
    blockPrint()
    
    institutions, classrooms, auditoriums = dict(), dict(), dict()
    # e1, e2 = EdInstitution("Innopolis"), EdInstitution("Kazan Federal")
    
    e1 = EdInstitution("Innopolis")

    institutions[e1.name] = e1
    # institutions[e2.name] = e2
    room1, audit1 = Klassroom(10, 1, True), LectureAuditorium(15, 1, False)
    room2, audit2 = Klassroom(10, 2, True), LectureAuditorium(15, 2, False)
    classrooms[1], classrooms[2] = room1, room2
    auditoriums[1], auditoriums[2] = audit1, audit2
    e1.add(room1)
    e1.add(audit1)
    # e2.add(room2)
    # e2.add(audit2)
    
    # Restore output here
    enablePrint()

    while True:
        
        print_welcome_menu()

        inp = int(input())
        if inp == 1:
            
            print_institutions_info()
            inst = get_institution(institutions)
            if not inst:
                print("institutions not exist\n")
            else:
                room_type = int(input("Enter (classroom - 1 or Auditorium - 2): "))
                
                if room_type == 1:
                    print("Enter (capacity, number, air conditioner- yes/no): ")
                    while True:
                        try:
                            capacity = int(input())
                            room_number = int(input())
                            conditioner = bool(int(input()))
                        except ValueError:
                            print("Not an integer! Try again.")
                            continue                            
                        else:
                            break
                    classroom = Klassroom(capacity, room_number, conditioner)
                    inst.add(classroom)
                    classrooms[room_number] = classroom
                    print(classroom)
                    print()
                
                elif room_type == 2:
                    print("Enter (capacity, number, air conditioner- yes/no): ")
                    while True:
                        try:
                            capacity = int(input())
                            room_number = int(input())
                            conditioner = bool(int(input()))
                        except ValueError:
                            print("Not an integer! Try again.")
                            continue                            
                        else:
                            break
                    audit = LectureAuditorium(capacity, room_number, conditioner)
                    inst.add(audit)    
                    auditoriums[room_number] = audit            
                    print(audit)
                    print()
                
                else:
                    print("Wrong Entry!")

        elif inp == 2:

            print_institution_summary(institutions)
            
        elif inp == 3:
            print("Choose one of the following Institution:\n")
            for instituion in institutions.keys():
                print(instituion)
            print()
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
                    while True:
                        try:
                            time_from_h, time_from_m, time_to_h, time_to_m, number_of_people = ask_time()
                        # How to stop it from rolling back
                        except ValueError:
                            print("Not an integer! Try again.")
                            continue                            
                        else:
                            break

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
                    while True:
                        try:
                            time_from_h, time_from_m, time_to_h, time_to_m, number_of_people = ask_time()
                        # How to stop it from rolling back
                        except ValueError:
                            print("Not an integer! Try again.")
                            continue                            
                        else:
                            break
                    time_from, time_to = convert_time(time_from_h, time_from_m, time_to_h, time_to_m)
                    choosen_audit.assign_activity(time_from, time_to, number_of_people)
                    print()     
            
        elif inp == 5:
            print_exit_summary(institutions)
            break           
        
        else:
            print("Wrong choice!")

