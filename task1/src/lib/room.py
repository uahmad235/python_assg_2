from datetime import datetime

class Room:
    """Interface for a Room"""

    def __init__(self, capacity: int, number: int, has_ac: bool, activites = []):
        self.capacity = capacity
        self.number = number
        self.has_ac = has_ac
        self.activites = activites

    def __str__(self):

        acts = '\n'.join(f'Activity assigned between {act[0]} and {act[1]}' for act in self.activites) 
        return f'''Room Type: {type(self).__name__}
        Room Number: {self.number}
        Capacity: {self.capacity}
        Air Conditioner? {"Installed" if self.has_ac else "Not Installed"}
        Activities: {'No Activity Assigned Yet!' if not acts.strip() else acts}'''

    def assign_activity(self, time_from, time_to, n_people):
        """
        Assign activity to the room based on user input times
        Parameters:
                time_from: time of starting of the activity
                time_to: time of ending of the activity
                n_people: number of people will participate in the activity

        """
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
        """
        Check if the room availabe in the choosen time [time from - time to]
        will used to check the availability of the room when assign activity by the user
        Parameters:
            time_from: time of starting of the activity
            time_to: time of ending of the activity
        """
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
        """
        Check if the current Room is available today or not
        Return [True] in case we have at least one hour gap between activities
        otherwise return not availabe today [False]
        """
        
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
    """Represents a classroom of the institution"""
    def __init__(self, capacity: int, number: int, has_ac: bool, activites = []):
        Room.__init__(self, capacity, number, has_ac, activites)

class LectureAuditorium(Room):
    """Represents an auditorium of the institution"""
    def __init__(self, capacity: int, number: int, has_ac: bool, activites = []):
        Room.__init__(self, capacity, number, has_ac, activites)