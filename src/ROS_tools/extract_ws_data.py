#!/usr/bin/env python2

import json
import rosbag
from datetime import datetime
from pprint import pprint

def extract_ws_data(bagfile_path, ws_topic_name, save_json_file):
    bag = rosbag.Bag(bagfile_path)

    print("Bag info:")
    print("\tstart: {} ({})".format(datetime.fromtimestamp(bag.get_start_time()), bag.get_start_time()))
    print("\t  end: {} ({})".format(datetime.fromtimestamp(bag.get_end_time()), bag.get_end_time()))
    print("\tduration: {}s".format(bag.get_end_time() - bag.get_start_time()))

    json_dict = {"car_states": []}
  
    cnt = 0
    for topic, msg, ts in bag.read_messages(topics=[ws_topic_name]):
        cnt += 1
        one_ws_state = {}
        one_ws_state["carState"] = {}
	one_ws_state["carState"]["wheelSpeeds"] = {}
        one_ws_state["carState"]["wheelSpeeds"]["fl"] = msg.wheel_fl;
        one_ws_state["carState"]["wheelSpeeds"]["fr"] = msg.wheel_fr;
        one_ws_state["carState"]["wheelSpeeds"]["rl"] = msg.wheel_rl;
        one_ws_state["carState"]["wheelSpeeds"]["rr"] = msg.wheel_rr;

        rostime_sec = msg.header.stamp.secs
        rostime_nsec = msg.header.stamp.nsecs
        stamp = str(rostime_sec).zfill(10)+ "." + str(rostime_nsec).zfill(9)
        one_ws_state["timestamp"] = stamp
        
        json_dict["car_states"].append(one_ws_state)

#    pprint(json_dict)
    print cnt        

    json_output = json.dumps(json_dict, indent=4)
#    print json_output
    with open(save_json_file, 'w') as f:
        f.write(json_output)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 4:
        extract_ws_data(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print "usage: extract_ws_data.py <bagfile> <ws_topic_name> <save_json_file>"
