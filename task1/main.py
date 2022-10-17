
from src.lib.room import Klassroom, LectureAuditorium
from src.lib.institution import EdInstitution
from src.helper.utils import convert_time
from src.helper import prompt_helper 
import os


STORAGE_FILE = 'task1/data/output'

def files_exist():
    """Check if all the storage files are on disk already"""
    extensions = ['.bak', '.dat', '.dir']
    return all([os.path.exists(STORAGE_FILE + ext) for ext in extensions])

def add_classrooms(inst: EdInstitution, classrooms: dict):
    """Add classrooms object to classrooms dictionary"""
    for classroom in inst.classrooms:
        classrooms[classroom.number] = classroom

def add_auditorium(inst: EdInstitution, auditoriums: dict):
    """Add auditorium object to auditoriums dictionary"""
    for audit in inst.auditoriums:
        auditoriums[audit.number] = audit

def main():
    """Entry point of the program"""
    # Block output at this point
    prompt_helper.blockPrint()
    
    institutions, classrooms, auditoriums = dict(), dict(), dict()

    if files_exist():
        print('Loading from storage path: ', STORAGE_FILE)
        e1 = EdInstitution('Innopolis')
        e1.restoreFromFile(STORAGE_FILE)

        e2 = EdInstitution('Kazan Federal')
        e2.restoreFromFile(STORAGE_FILE)
    else:
        print('Creating institutions from scratch')
        room1, audit1 = Klassroom(10, 1, True), LectureAuditorium(15, 1, False)
        room2, audit2 = Klassroom(10, 2, True), LectureAuditorium(15, 2, False)

        e1 = EdInstitution("Innopolis", set([room1]), set([audit1]))
        e2 = EdInstitution("Kazan Federal", set([room2]), set([audit2]))

        e1.add(room1)
        e1.add(audit1)
        e2.add(room2)
        e2.add(audit2)
    
    institutions[e1.name] = e1
    institutions[e2.name] = e2

    add_classrooms(e1, classrooms)
    add_classrooms(e2, classrooms)

    add_auditorium(e1, auditoriums)
    add_auditorium(e2, auditoriums)
    
    # Restore output here
    prompt_helper.enablePrint()

    while True:
        # prompt_helper.print_welcome_menu()
        inp = prompt_helper.get_main_menu_input()

        if inp == 1:
            prompt_helper.print_institutions_info(institutions)
            inst = prompt_helper.get_institution(institutions)
            prompt_helper.add_room_by_choice(prompt_helper.ask_room_information, classrooms, auditoriums, inst)
        elif inp == 2:
            prompt_helper.print_institution_summary(institutions)
        elif inp == 3:
            prompt_helper.assign_activities_classroom(institutions, classrooms)
        elif inp == 4:
            prompt_helper.assign_activity_auditorium(institutions, auditoriums)     
        elif inp == 5:
            prompt_helper.print_exit_summary(institutions)
            break
        else:
            print("Wrong choice!")

    for inst in institutions.values():
        inst.saveToFile(STORAGE_FILE)

if __name__ == "__main__":
    main()