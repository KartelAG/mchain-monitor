from time import sleep

from .systemstats import SystemStats

if __name__ == "__main__":
    test_obj = SystemStats()
    #need to sleep for cpu stat gatherings
    sleep(2)
    print(test_obj.get_stats())

__all__ = ["SystemStats"]