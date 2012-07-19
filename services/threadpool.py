from multiprocessing.dummy import Pool
from storage import StorageService
from time import sleep

def pool_params():
    null = 0

class ThreadPool(StorageService):
   

    def startup(self, thread_count):
        pool_params.thread_count = thread_count
        my_pool = Pool(thread_count)
        return my_pool
      
    def shutdown (self,arg_pool):
        
        arg_pool.close()
        arg_pool.join()
        
    def shutdown_dummy(self):
        sleep(1)
        
    
 

        
        