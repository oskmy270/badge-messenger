import os
import time

import badge

DEVICE = "/dev/ttyUSB0"
badgeMessage = "Hello world"
os.system("stty speed 38400 <" + DEVICE)
f = open(DEVICE, "w")
pkts = badge.build_packets(0x600, badge.message_file(badgeMessage, speed='4', action=badge.ACTION_ROTATE))
for p in pkts:
    f.write(p.format())
f.flush()
f.close()
