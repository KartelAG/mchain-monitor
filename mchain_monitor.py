import configparser
import datetime
import sys
import time
from threading import Thread

from web3 import Web3

from systemstats import SystemStats

class Mchain_Monitor():
    def __init__(self):
        try:
            self.__config = configparser.ConfigParser()
            self.__config.read('config.ini')
            self.error_log = open(self.__config['global']['error_filename'], 'a')
            if (self.__config['global']['stat_dest'] == 'file'):
                self.logger = LoggerToFile(self.__config['global']['filename'])
        except:
            self.error_log.write(''.join(str(datetime.datetime.now()), ' Error while init! Check config.ini and stat_dest option'))
            sys.exit()
        try:
            self.w3 = Web3(Web3.WebsocketProvider('ws://' + self.__config['global']['api_address'] + ':' + self.__config['global']['api_port']))
        except:
            self.error_log.write(''.join(str(datetime.datetime.now()), ' cannot connect to mchain node via ', self.__config['global']['api_address'], ':', self.__config['global']['api_port']))
        
    def log_event(self, event_data):
        self.logger.log_event(event_data)

    def log_loop(self, event_filter, poll_interval):
        while True:
            for event in event_filter.get_new_entries():
                self.log_event(str(event.hex()))
            time.sleep(poll_interval)

    def subscribe_for_new_blocks(self):
        self.block_filter = self.w3.eth.filter('latest')
        self.log_loop(self.block_filter, 1)

    def run(self):
        self.worker = Thread(target=self.subscribe_for_new_blocks, daemon=True)
        self.worker.start()


class LoggerToFile():
    def __init__(self, filename):
        self.filename = filename
        self.fd = open(self.filename, 'a')
    
    def log_event(self, event_data):
        self.fd.write(event_data)
        self.fd.write('\n')


if __name__ == '__main__':
    obj = Mchain_Monitor()
    #obj.run()
    obj.subscribe_for_new_blocks()
