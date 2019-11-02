from time import sleep

from systemstats import SystemStats

test_obj = SystemStats()
sleep(2)
print(test_obj.get_stats())