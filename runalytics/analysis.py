import pandas as pd
import numpy as np

def trimp(activity,rest_hr,max_hr):
    mins_per_hr = activity.groupby(by='heartrate').count()['time']/60
    hr = mins_per_hr.index
    hrr = (hr - rest_hr)/(max_hr - rest_hr)
    contributions = mins_per_hr * hrr * 0.64 * np.exp(hrr*1.92)
    return contributions.sum()
