import configparser
import datetime
import sys
import time
from threading import Thread

from web3 import Web3

from systemstats import SystemStats

class Mchain_Monitor():
    def __init__(self):
        self.error_log = open(self.__config['error_filename', 'a'])
        try:
            self.__config = configparser.ConfigParser()
            self.__config.read('config.ini')
            if (self.__config['stat_dest'] == 'file'):
                self.logger = LoggerToFile(self.__config['filename'])
        except:
            self.error_log.write(''.join(str(datetime.datetime.now()), ' Error while init! Check config.ini and stat_dest option'))
            sys.exit()
        try:
            self.w3 = Web3(Web3.WebsocketProvider('ws://' + self.__config['api_address'] + ':' + self.__config['api_port']))
        except:
            self.error_log.write(''.join(str(datetime.datetime.now()), ' cannot connect to mchain node via ', self.__config['api_address'], ':', self.__config['api_port']))
        
    def log_event(event_data):
        self.logger.log_event(event_data)

    def log_loop(event_filter, poll_interval):
        while True:
            for event in event_filter.get_new_entries():
                self.log_event(event)
            time.sleep(poll_interval)

    def subscribe_for_new_blocks():
        self.block_filter = self.w3.eth.filter('latest')
        self.log_loop(self.block_filter, 0)

    def run():
        self.worker = Thread(target=subscribe_for_new_blocks, daemon=True)
        self.worker.start()


class LoggerToFile(filename):
    def __init__(self, filename):
        try:
            self.__fd == open(filename, 'a')
        except:
            self.error_log.write(''.join(str(datetime.datetime.now()), ' Error opening log file!'))
            sys.exit()
    
    def log_event(event_data):
        self.__fd.write(event_data)

