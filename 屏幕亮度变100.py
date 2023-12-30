# import wmi
# c = wmi.WMI(namespace='root\WMI')
 
# a = c.WmiMonitorBrightnessMethods()[0]
# a.WmiSetBrightness(Brightness=80, Timeout=500) # Brightness：亮度

import screen_brightness_control as sbc

sbc.set_brightness(100)