import os
import time

import badge

DEVICE = "/dev/ttyUSB0"
badgeMessage = "Hello world"
L = [216, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100]
badgeMessage = ''.join(chr(i) for i in L)
os.system("stty speed 38400 <" + DEVICE)
f = open(DEVICE, "w")
pkts = badge.build_packets(0x600, badge.message_file(badgeMessage, speed='4', action=badge.ACTION_ROTATE))
for p in pkts:
    f.write(p.format())
f.flush()
f.close()
