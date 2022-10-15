

from room import Klassroom, LectureAuditorium
from institution import EdInstitution
from utils import convert_time
import prompt_helper 


def main():
    # Block output at this point
    prompt_helper.blockPrint()
    
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
    prompt_helper.enablePrint()

    while True:
        prompt_helper.print_welcome_menu()
        inp = int(input())
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

if __name__ == "__main__":
    main()
