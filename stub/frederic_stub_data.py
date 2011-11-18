#!/usr/bin/env python
import env
from models.webpage import Webpage
from models.user import User
from models.tracker import Tracker
from models.tracker_group import TrackerGroup
from services.tracker import TrackerService
from datetime import datetime, timedelta
from database.sqlalch import Session

def populate():
    service = TrackerService(None)
    session = Session()
  
    u = User(email='bazin.frederic@gmail.com', first_name='fred',
            last_name='bazin',password='test')
    session.add_all([u])
    session.commit()
    session.refresh(u)

    # Tracker groups
    tg1 = TrackerGroup(name='test', user_id=u.id)
    tg2 = TrackerGroup(name='bugs', user_id=u.id)
    session.add_all([tg1,tg2])
    session.commit()
    session.refresh(tg1)
    session.refresh(tg2)

    t1 = Tracker(name='bbc uk', url='http://www.bbc.co.uk', 
            frequency=300, tracker_group_id=tg1.id,
            css_selector='#div-div-div-div-div-div-div-div_2')
    t2 = Tracker(name='lemonde', url='http://www.lemonde.fr', 
            frequency=60, tracker_group_id=tg1.id,
            css_selector='#rub_rub_sport')
    t3 = Tracker(name='twit', url='http://www.freelancer.com', 
            frequency=300, tracker_group_id=tg1.id,
            css_selector='#pg-lnd')
    t4 = Tracker(name='nfl.com', url='http://www.nfl.com', 
            frequency=300, tracker_group_id=tg1.id,
            css_selector='body')
    t5 = Tracker(name='laurel', url='http://www.bloglaurel.com', 
            frequency=300, tracker_group_id=tg2.id,
            css_selector='body')
    service.insert(t1)
    service.insert(t2)
    service.insert(t3)
    service.insert(t4)
    service.insert(t5)
    session.commit()
   

if __name__ == '__main__':
    populate()
