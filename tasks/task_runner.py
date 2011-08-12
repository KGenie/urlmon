from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Process, Queue


class TaskRunner(object):

    def __init__(self, thread_count, mail_queue):
        self.output = Queue()
        self.worker = Process(target=runner, args=(self.output, thread_count,
            mail_queue))
        self.worker.daemon = True
        self.worker.start()


    def run_task(self, task):
        self.output.put(task)


def runner(input, thread_count, mail_queue):
    pool = ThreadPool(thread_count)

    while 1:
        task = input.get()
        pool.apply_async(run, args=(task,))


def run(task, mail_queue):
    if task.name == 'RETRIEVE_URL':
        pass
    elif task.name == 'CHECK_AND_NOTIFY':
        pass
