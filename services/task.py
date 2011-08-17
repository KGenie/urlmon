from datetime import datetime, timedelta
from storage import StorageService
from models.task import TrackResource, UpdateResource

text=""" elcome to my Small-But-Intense Home Page! There's not
much here yet, but at least I'm avoiding those obnoxious under construction tags, so if
there's a
visible link it should give you something. """

class TaskService(StorageService):

    @classmethod
    def stub_data(cls):
        pass
#        cls.insert(UpdateResource(url='http://dustyfeet.com',
#            next_run=datetime.now() + timedelta(seconds=20)))
#        cls.insert(TrackResource(tracker_id=1, 
#            last_content=text,
#            next_run=datetime.now() + timedelta(seconds=5)))


    @classmethod
    def get_tasks_to_run(cls):
        tasks = cls.get_all()
        now = datetime.now()
        return (t for t in tasks if t.next_run <= now)
