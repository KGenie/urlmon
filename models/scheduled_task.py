# Code based on 
# http://stackoverflow.com/questions/373335/suggestions-for-a-cron-like-scheduler-in-python
from app_components.model import Model
from tasks.task import Task


class AllMatch(set):
    def __contains__(self, item): return True


def to_set(obj):
    is isinstance(obj, (int,long)):
        return set([obj])
    if not isinstance(obj, set):
        return set(obj)
    return obj


__all_match = AllMatch()

class ScheduledTask(Model):

    def __init__(self, id, name, args, minutes, hours, days, months, 
            days_of_week):
        self.id = id
        self.name = name
        self.args = args
        self.minutes = to_set(minutes) or __all_match
        self.hours = to_set(hours) or __all_match
        self.days = to_set(days) or __all_match
        self.months = to_set(months) or __all_match
        self.days_of_week = to_set(days_of_week) or __all_match


    def match(self, datetime):
        return ((datetime.minute     in self.minutes) and
                (datetime.hour       in self.hours) and
                (datetime.day        in self.days) and
                (datetime.month      in self.months) and
                (datetime.weekday()  in self.days_of_week))
