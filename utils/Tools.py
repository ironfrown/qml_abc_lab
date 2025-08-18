# Support functions for QML and QNN demos
# Author: Jacob Cybulski, ironfrown[at]gmail.com
# Date: September 2024

import os
import math
import numpy as np

####### Useful functions

### Returns the current date and time
import datetime

def get_timestamp_now():
    now = datetime.datetime.now()
    now_date = (now.year, now.month, now.day)
    now_time = (now.hour, now.minute, now.second)
    time_stamp = f'%04d-%02d-%02d %02d:%02d:%02d' % (now_date + now_time)
    return time_stamp

### Add absolute noise to TS
#   X_ts: TS X axis
#   y_ts: TS y axis
#   noise: Maximum +/- noise level 
def add_noise(vec, noise=0.0):
    if noise == 0:
        return vec
    else:
        rng = np.random.default_rng()
        noise_vec = np.random.uniform(-1, 1, len(vec))*noise
        noise_vec = [y+e for (y, e) in zip(vec, noise_vec)]
        return np.array(noise_vec)
