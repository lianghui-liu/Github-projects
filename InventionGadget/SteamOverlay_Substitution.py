from PIL import ImageGrab
import psutil
import win32process
import win32gui
import datetime
import keyboard
import time
from plyer import notification
import winsound


import os
import glob
from PIL import Image
from ctypes import wintypes
import ctypes
import sys
 
 
argvs=sys.argv
default_key='del'
if len(argvs)>1:
    if argvs[1]=='f12':
        default_key='f12'
        print("Default binding key changed to: ",default_key)

print(argvs)

duration = 1000  # millisecond
freq = 440  # Hz

# print(0)
# keyboard.wait('a')
# #在按下a之前后面的语句都不会执行，下面同理
# print(1)
# keyboard.wait('b')
# print(2)
# keyboard.wait('c')
# print(3)
# keyboard.wait()

#继续监听
#只有按顺序按下abc（中间过程随便按不干扰）才能输出0123，但因为最后一个没设置按键，所以会一直监听下去



# # title = win32gui.GetWindowText (win32gui.GetForegroundWindow())



# toplist, winlist = [], []
# def enum_cb(hwnd, results):
#     winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
# win32gui.EnumWindows(enum_cb, toplist)

# firefox = [(hwnd, title) for hwnd, title in winlist if 'firefox' in title.lower()]
# # just grab the hwnd for first window matching firefox
# firefox = firefox[0]
# hwnd = firefox[0]

#获取前台窗口的句柄
handle = None

# hread_id, process_id = win32process.GetWindowThreadProcessId(handle) 

# 检测当前句柄是否存在  存在则返回  1  不存在返回 0
# N = win32gui.IsWindowEnabled("句柄值")
# S = win32gui.IsWindowVisible("句柄值")
# V = win32gui.IsWindow("句柄值")

# #根据前台窗口的句柄获取线程tid和进程pid
# tid, pid = win32process.GetWindowThreadProcessId(handle)

# #根据前台窗口的进程pid获取进程名称
# process_name = psutil.Process(pid).name()

# 获取真实的窗口 POS
def get_window_rect(hwnd):
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f:
        rect = ctypes.wintypes.RECT()
        f(ctypes.wintypes.HWND(hwnd), ctypes.wintypes.DWORD(9), ctypes.byref(rect), ctypes.sizeof(rect))
        return (rect.left, rect.top, rect.right, rect.bottom)


# x, y, z, b = get_window_rect(hwnd)


def takeScreenshot():
    global handle
    if handle==None:
        handle = win32gui.GetForegroundWindow()
    bbox = get_window_rect(handle)
    # bbox = win32gui.GetWindowRect(handle)
    img = ImageGrab.grab(bbox)
    dirPath="D:\\Steam\\userdata\\1277566364\\760\\remote\\16331844908098781184\\screenshots\\"
    fileName=f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    filePath=dirPath+fileName
    if not os.path.exists(dirPath+"thumbnails\\"):
        os.makedirs(dirPath+"thumbnails\\")
    thumbpath=dirPath+"thumbnails\\"+fileName+'.ico'
    img.save(filePath+'.jpg')
    # img.show()
    # ratio=150/img.width
    # img.thumbnail((150,img.height*ratio))
    img.thumbnail((50,50))
    # img.show()
    # input(thumbpath+'.ico')

    img.save(thumbpath)
    img.close()
    winsound.Beep(freq, duration)
    notification.notify(
        title="Done !",
        message="Take Screenshot",
        app_name="MySteamOverlay", 
        app_icon=thumbpath,
        timeout=1
    )
    # notify(title=”, message=”, app_name=”, app_icon=”, timeout=10, ticker=”, toast=False)

# def thumbnail_pic(path):
#     #glob.glob(pathname)，返回所有匹配的文件路径列表
#     a=glob.glob(r'./img/*.jpg')
#     for x in a:
#         name=os.path.join(path,x)
#         im=Image.open(name)
#         im.thumbnail((80,80))
#         print(im.format,im.size,im.mode)
#         im.save(name,'JPEG')
#     print('Done!')

# if __name__=='__main__':
#     path='.'
#     thumbnail_pic(path)
def isAlive():
    return win32gui.IsWindow(handle)

run=True

def endNotify(howKilled):
    '''controledKill 1,no alive window 2'''
    global run
    run=False
    winsound.Beep(freq, duration)
    match howKilled:
        case 1:
            notification.notify(
            title="Thread Dead",
            message="controledKill",
            # app_icon="tubiao.ico",
            timeout=1
        )
        case 2:
            notification.notify(
            title="Thread Dead",
            message="noWindowAlive",
            # app_icon="tubiao.ico",
            timeout=1
        )
        

if __name__ == '__main__':
    # a=glob.glob(r'./img/*.jpg')
    # for x in a:
    #     name=os.path.join('.',x)
    #     #     print(name)
    keyboard.add_hotkey(default_key, takeScreenshot)
    keyboard.add_hotkey('ctrl+f12', endNotify,(1,))
    while run:
        if handle!=None and isAlive()!=1:
            endNotify(2)
        time.sleep(5)
    
    print('System exited, be good !')
    #按f1输出aaa
    #按ctrl+alt输出b
    #wait里也可以设置按键，说明当按到该键时结束
    # keyboard.wait()

# win32gui.SetForegroundWindow(hwnd)
# bbox = win32gui.GetWindowRect(handle)
# img = ImageGrab.grab(bbox)
# img.save(f"D:\\Steam\\userdata\\1277566364\\760\\remote\\16331844908098781184\\screenshots\\{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
# img.show()