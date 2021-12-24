
from datetime import datetime
import time

def utc2local_offset():
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return offset