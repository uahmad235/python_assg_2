import os
import sys
from room import Klassroom, LectureAuditorium
from utils import convert_time

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def print_institutions_info(institutions):
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
    print_institutions_info(institutions)
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
    while True:
        try:
            time_from_h = int(input("Please enter the hour of starting "))
            time_from_m = int(input("Please enter the minute of starting "))

            time_to_h = int(input("Please enter the hour of ending "))
            time_to_m = int(input("Please enter the minute of ending "))

            number_of_people = int(input("Please enter number of attendance "))
        except ValueError:
            print("Not an integer! Try again.")
        else:
            break
    return time_from_h,time_from_m,time_to_h,time_to_m,number_of_people
    

def ask_room_information():
    while True:
        user_input = input("Enter (capacity, number, air conditioner- yes/no): ")

        user_inputs = user_input.split(' ')
        if len(user_inputs) < 3:
            print("Enter all the required fields...")
        else:
            try:
                capacity = int(user_inputs[0])
                room_number = int(user_inputs[1])
                conditioner = user_inputs[2] == 'yes'
            except ValueError:
                print("Not an integer! Try again.")                           
            else:
                break

    return capacity,room_number,conditioner


def add_room_by_choice(ask_room_information, classrooms, auditoriums, inst):
    if not inst:
        print("institutions not exist\n")
    else:
        room_type = int(input("Enter (classroom - 1 or Auditorium - 2): "))
                
        capacity, room_number, conditioner = ask_room_information()

        if room_type == 1:
            classroom = Klassroom(capacity, room_number, conditioner)
            inst.add(classroom)
            classrooms[room_number] = classroom
            print(classroom)
        elif room_type == 2:
            audit = LectureAuditorium(capacity, room_number, conditioner)
            inst.add(audit)    
            auditoriums[room_number] = audit            
            print(audit)
        else:
            print("Wrong Entry!")
        print()

def assign_activities_classroom(institutions, classrooms):
    print("Choose one of the following Institution:\n")
    for instituion in institutions.keys():
        print(instituion)
    print()
    instituion = get_institution(institutions)
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
            time_from_h, time_from_m, time_to_h, time_to_m, number_of_people = ask_time()
            time_from, time_to = convert_time(time_from_h, time_from_m, time_to_h, time_to_m)
            choosen_room.assign_activity(time_from, time_to, number_of_people)
            print()

def assign_activity_auditorium(institutions, auditoriums):
    print("Choose one of the following Institution:\n")
            
    for instituion in institutions.values():
        print(instituion.name)
    instituion = get_institution(institutions)
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
            time_from_h, time_from_m, time_to_h, time_to_m, number_of_people = ask_time()
            time_from, time_to = convert_time(time_from_h, time_from_m, time_to_h, time_to_m)
            choosen_audit.assign_activity(time_from, time_to, number_of_people)
            print()
