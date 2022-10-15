from datetime import datetime

class Room:
    """Interface for a Room"""

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
        
        if time_from < datetime.now().replace(hour = 8, minute = 0) or time_from > datetime.now().replace(hour = 21, minute = 0):
            print("You should enter time between 8 to 21")
        elif self.capacity < n_people:
            print(f"Room number {self.number} can't fit for {n_people} people, max capacity is {self.capacity}")
        elif time_from > time_to:
            print("Ending hours can't be smaller than starting hours...")
        
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

        sorted_act = sorted(self.activites)
        if len(self.activites) == 1:
            return (sorted_act[0][1] - sorted_act[0][0]).seconds / (60*60) < 12

        for i in range(len(sorted_act) - 1):
            duration = sorted_act[i + 1][0] - sorted_act[i][1]
            duration_in_s = duration.total_seconds()
            hours = divmod(duration_in_s, 3600)[0] 
            if hours >= 1:
                return True

        return False


class Klassroom(Room):
    
    def __init__(self, capacity: int, number: int, has_ac: bool, activites = []):
        Room.__init__(self, capacity, number, has_ac, activites)

class LectureAuditorium(Room):
    
    def __init__(self, capacity: int, number: int, has_ac: bool, activites = []):
        Room.__init__(self, capacity, number, has_ac, activites)
