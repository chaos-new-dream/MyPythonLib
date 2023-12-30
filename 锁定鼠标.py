import win32api
import time
# 定义矩形的左上角和右下角坐标
left, top, right, bottom = 0, 1, 1920, 1080

# 创建矩形对象
rect = (left, top, right, bottom)
while True:
	win32api.ClipCursor(rect)
	time.sleep(0.5)
# time.sleep(10)
# try:
#     # 限制鼠标光标的移动范围
#     win32api.ClipCursor(rect)
# except KeyboardInterrupt:
#     # 取消限制，恢复正常的鼠标光标移动范围
#     win32api.ClipCursor(None)
# win32api.ClipCursor(None)