from sqlalchemy import Table, MetaData, Column, Index, ForeignKey, Boolean,\
        Integer, String, DateTime, LargeBinary, PickleType
from custom_types import StringList

metadata = MetaData()


webpage = Table('webpage', metadata,
        # 2083 is the maximum url length supported by IE
        Column('url', String(2083), primary_key=True),
        Column('contents', LargeBinary),
        Column('last_updated', DateTime),
        Column('digest', LargeBinary(20))
        )


user = Table('user', metadata,
        # 320 seems to be the maximum length of email addresses
        Column('email', String(320), primary_key=True),
        Column('first_name', String(50)),
        Column('last_name', String(50)),
        Column('password', String(50)),
        Column('roles', StringList(200)),
        Column('last_login', DateTime)
        )


registration = Table('registration', metadata,
        Column('reg_id', String(40), primary_key=True),
        Column('email', String(320), unique=True, index=True),
        Column('user', PickleType)
        )


tracker_group = Table('tracker_group', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(75)),
        Column('comment', String(550)),
        Column('user_email', ForeignKey('user.email'))
        )
Index('idx_name_user', tracker_group.c.name, tracker_group.c.user_email,
        unique=True)


tracker = Table('tracker', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(75)),
        Column('comment', String(550)),
        Column('frequency', Integer),
        Column('css_selector', String(300)),
        Column('url', ForeignKey('webpage.url')),
        Column('tracker_group_id', ForeignKey('tracker_group.id')),
        )


task = Table('task', metadata,
        Column('id', Integer, primary_key=True),
        Column('next_run', DateTime),
        Column('is_running', Boolean),
        Column('type', Integer)
        )


track_resource = Table('track_resource', metadata,
        Column('id', ForeignKey('task.id'), primary_key=True),
        Column('tracker_id', ForeignKey('tracker.id')),
        Column('last_content', LargeBinary),
        Column('last_digest', LargeBinary(20))
        )


update_resource = Table('update_resource', metadata,
        Column('id', ForeignKey('task.id'), primary_key=True),
        Column('url', ForeignKey('webpage.url'), unique=True)
        )
