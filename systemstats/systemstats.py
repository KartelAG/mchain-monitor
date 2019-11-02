import os
import psutil
import json
from time import sleep

class SystemStats():
    def __init__(self):
        self.stats = {}
        self.stats['uname'] = os.uname()
        self.stats['cpu_count'] = psutil.cpu_count()
        self.stats['mem_total'] = psutil.virtual_memory().total
        self.stats['disk_info'] = {}
        disk_list = psutil.disk_partitions()
        for i in range(0,len(disk_list)):
            disk_path = disk_list[i].mountpoint
            self.stats['disk_info'][disk_path] = psutil.disk_usage(disk_path)
        self.__update_stats()    
    
    def __update_stats(self):
        self.stats['cpu_load'] = psutil.cpu_percent()
        self.stats['mem_load'] = psutil.virtual_memory().percent
        disk_list = psutil.disk_partitions()
        for i in range(0,len(disk_list)):
            disk_path = disk_list[i].mountpoint
            self.stats['disk_info'][disk_path] = psutil.disk_usage(disk_path)
                
    def get_stats(self):
        self.__update_stats()
        return json.dumps(self.stats)



