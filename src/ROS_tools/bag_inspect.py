#!/usr/bin/env python2

import rosbag
from datetime import datetime

def inspect(bagfile_path):
    bag = rosbag.Bag(bagfile_path)
    print("Bag info:")
    print("\tstart: {} ({})".format(datetime.fromtimestamp(bag.get_start_time()), bag.get_start_time()))
    print("\t  end: {} ({})".format(datetime.fromtimestamp(bag.get_end_time()), bag.get_end_time()))
    print("\tduration: {}s".format(bag.get_end_time() - bag.get_start_time()))
    print("topic,\t\t\"latency\",\tbag stamp,\t\theader stamp")
    for topic, msg, t in bag.read_messages():
        if hasattr(msg, "header"):
	    rostime = msg.header.stamp
            rostime_sec = msg.header.stamp.secs
            rostime_nsec = msg.header.stamp.nsecs
        elif hasattr(msg, "transforms"):
            rostime = msg.transforms[0].header.stamp
	else:
	    print("what??")	

        if rostime:
            header_stamp = rostime.to_sec()
            header_stamp_datetime = datetime.fromtimestamp(header_stamp)
        else:
            header_stamp = ""
            header_stamp_datetime = ""
        
        if header_stamp:
            latency = t.to_sec() - header_stamp
        else:
            latency = ""
	
	try:
            print("{},\t{}s, {} ({}), {} ({:.6f}, {}, {})".format(
                topic,
                latency,
                datetime.fromtimestamp(t.to_sec()),
                t.to_sec(),
                header_stamp_datetime,
                header_stamp,
		rostime_sec,
		rostime_nsec
            ))
	except Exception, e:
	    print e

if __name__ == '__main__':
  import sys
  if len(sys.argv) == 2:
    inspect(sys.argv[1])
  else:
    print('usage: bag_inspect.py <bagfile>')

