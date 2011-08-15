# Code based on 
# http://stackoverflow.com/questions/373335/suggestions-for-a-cron-like-scheduler-in-python

from app_components.model import Model


class AllMatch(set):
    def __contains__(self, item): return True

allmatch = AllMatch()


class TaskType:
    UPDATE_RESOURCE = 1
    CHECK_MODIFICATION = 2


class Task(Model):

    def __init__(self, id=None, type=None, args=None, 
            minutes=None, hours=None, days=None, 
            months=None, days_of_week=None):

        self.id = id
        self.type = type
        self.args = args
        self.minutes = to_set(minutes) or allmatch
        self.hours = to_set(hours) or allmatch
        self.days = to_set(days) or allmatch
        self.months = to_set(months) or allmatch
        self.days_of_week = to_set(days_of_week) or allmatch


    def match(self, datetime):
        return True
        #return ((datetime.minute     in self.minutes) and
        #        (datetime.hour       in self.hours) and
        #        (datetime.day        in self.days) and
        #        (datetime.month      in self.months) and
        #        (datetime.weekday()  in self.days_of_week))



def to_set(obj):
    if not obj:
        return None
    if isinstance(obj, (int,long)):
        return set([obj])
    if not isinstance(obj, set):
        return set(obj)
    return obj
