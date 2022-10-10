from typing import List
from abc import ABC, abstractmethod
from datetime import datetime



class Activity:

    title: str
    time: datetime.date

    def __init__(self, title, time):
        pass


class Room(ABC):
    """Abstract interface for a Room"""
    capacity: int
    number: int
    has_ac: bool
    assigned_activities: List[Activity]

    def __init__(self, number, capacity, has_ac, activities) -> None:
        pass

    def assign_activity(new_activity: Activity):
        """Assign activity at certain time if that slot is available"""
        pass


class Klassroom(Room):
    pass


class LectureAuditorium(Room):
    pass


class EdInstitution:

    name: str
    klassrooms: List[Klassroom]
    auditoriums: List[LectureAuditorium]

    def add(self):
        pass
        
    def remove(self):
        pass

    def saveToFile(self, file_name):
        """Dump all the object data in .txt file."""
        pass
    
    def restoreFromFile(self):
        """restore the object data from a .txt file."""
        pass
