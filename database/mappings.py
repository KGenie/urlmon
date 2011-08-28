import tables
from sqlalchemy.orm import mapper, relationship, backref
from models.webpage import Webpage
from models.webpage_version import WebpageVersion
from models.user import User
from models.registration import Registration
from models.tracker_group import TrackerGroup
from models.tracker import Tracker
from models.task import Task
from models.tracker_change import TrackerChange
from models.track_resource import TrackResource
from models.update_resource import UpdateResource

mapper(Webpage, tables.webpage,
        properties={
            '_url': tables.webpage.c.url
            })


mapper(WebpageVersion, tables.webpage_version,
        properties={
            '_url': tables.webpage_version.c.url,
            '_content': tables.webpage_version.c.content
            })
            

mapper(User, tables.user,
        properties={
            '_pass': tables.user.c.password
            })


mapper(Registration, tables.registration,
        properties={
            '_user': tables.registration.c.user
            })


mapper(TrackerGroup, tables.tracker_group,
        properties={
            'user': relationship(User, lazy='join')
            })


mapper(Tracker, tables.tracker,
        properties={
            '_url': tables.tracker.c.url,
            'tracker_group': relationship(TrackerGroup, lazy='join',
            backref=backref('trackers', order_by=tables.tracker.c.id)),
            'webpage': relationship(Webpage, lazy='select')
            })


mapper(Task, tables.task, 
        polymorphic_on=tables.task.c.type,
        polymorphic_identity=0)


mapper(TrackerChange, tables.tracker_change,
        properties={
            'tracker': relationship(Tracker),
            'webpage_version': relationship(WebpageVersion),
            '_content': tables.tracker_change.c.content
            })


mapper(TrackResource, tables.track_resource,
        inherits=Task,
        properties={
            'tracker': relationship(Tracker)
            },
        polymorphic_identity=1)

mapper(UpdateResource, tables.update_resource,
        inherits=Task,
        properties={
            'webpage': relationship(Webpage)
            },
        polymorphic_identity=2)

