from sqlalchemy import Table, MetaData, Column, ForeignKey, Boolean,\
        Integer, String, DateTime, LargeBinary
from custom_types import StringList

metadata = MetaData()


webpage = Table('webpage', metadata,
        # 2083 is the maximum url length supported by IE
        Column('url', String(2083), primary_key=True),
        Column('contents', LargeBinary),
        Column('last_modified', DateTime)
        )


user = Table('user', metadata,
        # 320 seems to be the maximum length of email addresses
        Column('email', String(320), primary_key=True),
        Column('first_name', String(50)),
        Column('last_name', String(50)),
        Column('password', String(50)),
        Column('active', Boolean),
        Column('roles', StringList(200)),
        Column('last_login', DateTime)
        )


tracker_group = Table('tracker_group', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(75)),
        Column('comment', String(225)),
        Column('user_email', ForeignKey('user.email'))
        )


tracker = Table('tracker', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(75)),
        Column('frequency', Integer),
        Column('css_selector', String(300)),
        Column('url', ForeignKey('webpage.url')),
        Column('tracker_group_id', ForeignKey('tracker_group.id')),
        Column('user_email', ForeignKey('user.email'))
        )


task = Table('task', metadata,
        Column('id', Integer, primary_key=True),
        Column('next_run', DateTime),
        Column('type', Integer)
        )


track_resource = Table('track_resource', metadata,
        Column('id', ForeignKey('task.id'), primary_key=True),
        Column('tracker_id', ForeignKey('tracker.id')),
        Column('last_content', LargeBinary)
        )


update_resource = Table('update_resource', metadata,
        Column('id', ForeignKey('task.id'), primary_key=True),
        Column('url', ForeignKey('webpage.url'))
        )
