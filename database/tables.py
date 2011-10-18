from sqlalchemy import Table, MetaData, Column, Index, ForeignKey, Boolean,\
        Integer, String, DateTime, LargeBinary, PickleType
from custom_types import StringList, GzipBlob

metadata = MetaData()

#./controllers/tracker.py
#./controllers/tracker_group.py
#./services/tracker.py
#./services/tracker_group.py
#./populate_database.py
#./database/tables.py
#./models/tracker_group.py


webpage = Table('webpage', metadata,
        # 2083 is the maximum url length supported by IE
        Column('url', String(2083), primary_key=True),
        Column('last_checked', DateTime)
        )


webpage_version = Table('webpage_version', metadata,
        Column('id', Integer, primary_key=True),
        Column('url', ForeignKey('webpage.url')),
        Column('content', GzipBlob),
        Column('digest', LargeBinary(20)),
        Column('date', DateTime)
        )
Index('idx_webpage_date', webpage_version.c.date)


user = Table('user', metadata,
        Column('id', Integer, primary_key=True),
        # 320 seems to be the maximum length of email addresses
        Column('email', String(320), unique=True, index=True),
        Column('first_name', String(50)),
        Column('last_name', String(50)),
        Column('password', LargeBinary(64)),
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
        Column('user_id', ForeignKey('user.id'))
        )
Index('idx_name_user', tracker_group.c.name, tracker_group.c.user_id,
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


tracker_change = Table('tracker_change', metadata,
        Column('id', Integer, primary_key=True),
        Column('tracker_id', ForeignKey('tracker.id')),
        Column('webpage_version_id', ForeignKey('webpage_version.id')),
        Column('content', GzipBlob),
        Column('digest', LargeBinary(20)),
        Column('current_css_selector', String(300)),
        Column('start_index', Integer)
        )


track_resource = Table('track_resource', metadata,
        Column('id', ForeignKey('task.id'), primary_key=True),
        Column('tracker_id', ForeignKey('tracker.id'))
        )


update_resource = Table('update_resource', metadata,
        Column('id', ForeignKey('task.id'), primary_key=True),
        Column('url', ForeignKey('webpage.url'), unique=True)
        )
