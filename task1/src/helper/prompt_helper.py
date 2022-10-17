import os
import sys
from src.lib.room import Klassroom, LectureAuditorium
from .utils import convert_time


def blockPrint():
    """
    Block the standard output
    """
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    """
    Restore the standard output
    """
    sys.stdout = sys.__stdout__


def get_main_menu_input():
    """Prompts for taking input for main menu"""
    while True:
        print_welcome_menu()
        try:
            inp = int(input())
            if inp < 1 or inp > 5:  # No out of range
                raise ValueError() 
            return inp
        except ValueError:
            # Either the input is invalid integer choice or is a string
            print("\nInvalid Choice. Please input a valid number between 1 and 5 !")


def print_institutions_info(institutions):
    """
    Print list of instituitons we have in the system
    Parameters:
            institutions: dictionary of all institutions in the system
    """
    print("we have the following instituions in the system:\n")
    for institution in institutions.keys():
        print(institution)
    print()


def print_welcome_menu():
    """
    Print menu which contains list of options for the user to choose from
    """
    print("\nChoose one operation from below :")
    print("1 : Add classroom or Auditorium to institution")
    print("2 : Print institution summary")
    print("3 : Assign activity to classroom")
    print("4 : Assign activity to LectureAuditorium")
    print("5 : Exit program")

def get_institution(institutions):
    """
    Get the name of the institution from input pipe 
    and return and information about this insitituion
    """
    inst_name = input("Enter institution name : ")
    inst = institutions.get(inst_name, False)
    return inst

def print_institution_summary(institutions):
    """
    Print the information of the selected instistuion
    Parameters:
        institutions: dictionary of all institutions in the system
    Output: 
        Number of Classroms
        Number of Auditoriums
        Status for Today
    """
    print_institutions_info(institutions)
    inst = get_institution(institutions)
    if not inst:
        print("institutions not exist\n")
    else:
        print(inst)

def print_exit_summary(institutions):
    """
    Print summary of every instituon in the databaset we have
    Output: 
        Number of Classroms
        Number of Auditoriums
        Status for Today [for each institution]
    """
    print("In database we have:")
    for institution in institutions:
        print(institutions[institution])

def ask_time():
    """
    Get time and number of people of activity from the user input
    it will expect five input numbers
    Input: 
        time_from_h: [Integer] hour of starting of the activity
        time_from_m: [Integer] minute of starting of the activity
        time_to_h:   [Integer] hour of ending of the activity
        time_to_m:   [Integer] minute of ending of the activity
        number_of_people: [Integer] Number of people that will participate in this activity

    """
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
    """
    Get information about the room the user wished to add to the institution
    it will expect three input numbers
    Input: 
        capacity: [Integer] hour of starting of the activity
        number: [Integer] number of the room
        conditioner: [String] indicator if air contition is installed or not.
    """
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
    """
    Add room to the institution based on user choosen type
    Parameters:
    ask_room_information: Function to extract information about the room from the user
    classrooms: Dictionary to hold the information about classrooms we have in the system
    auditoriums: Dictionary to hold the information about auditoriums we have in the system
    inst: the institution the user want to add room to it.
    """
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
    """
    Assign the activity to classroom
    Parameters:
            institutions: dictionary of all instituions objects we have in the system
            classrooms: dictionary of all classrooms objects we have this instituion
    """
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
    """
    Assign the activity to auditorium
    Parameters:
            institutions: dictionary of all instituions objects we have in the system
            auditorium: dictionary of all auditoriums objects we have this instituion
    """
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
