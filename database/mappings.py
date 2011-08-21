import tables
from sqlalchemy.orm import mapper, relationship, backref
from models.webpage import Webpage
from models.user import User
from models.tracker_group import TrackerGroup
from models.tracker import Tracker
from models.task import Task
from models.track_resource import TrackResource
from models.update_resource import UpdateResource

mapper(Webpage, tables.webpage,
        properties={
            '_url': tables.webpage.c.url,
            '_contents': tables.webpage.c.contents
            })

mapper(User, tables.user)

mapper(TrackerGroup, tables.tracker_group,
        properties={
            'user': relationship(User, lazy='join')
            })

mapper(Tracker, tables.tracker,
        properties={
            'tracker_group': relationship(TrackerGroup, lazy='join',
            backref=backref('trackers', order_by=tables.tracker.c.id)),
            'webpage': relationship(Webpage, lazy='select')
            })

mapper(Task, tables.task, 
        polymorphic_on=tables.task.c.type,
        polymorphic_identity=0)

mapper(TrackResource, tables.track_resource,
        inherits=Task,
        properties={
            'tracker': relationship(Tracker),
            '_last_content': tables.track_resource.c.last_content
            },
        polymorphic_identity=1)

mapper(UpdateResource, tables.update_resource,
        inherits=Task,
        properties={
            'webpage': relationship(Webpage)
            },
        polymorphic_identity=2)

