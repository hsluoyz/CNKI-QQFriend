# coding=gbk

import win32con
import win32gui
import win32api
import win32clipboard
import os
import time
import re

try:
    import user_data
    user_list = user_data.user_list
    qq_shortcut = user_data.qq_shortcut
except:
    print 'No user data, use default value'
    user_list = {}
    user_list['ly'] = {'name': 'ly', 'email': 'xxx@something.com', 'spell': 'osvtzhuli'}
    qq_shortcut = '"C:\Program Files (x86)\Tencent\QQ\Bin\QQScLauncher.exe" /uin:XXXXXXXXX /quicklunch:449BDE2DE4BA357E6E9168FD55AB24059BB3CABB1EEF93699642E5891DC173715F5B4E3EDF68B41F'

# Set the clipboard with a str.
def QQ_setClipboardText(str):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_TEXT, str)
    win32clipboard.CloseClipboard()

# Print plain text.
def QQ_PrintText(str):
    QQ_setClipboardText(str.encode('gbk'))
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0);
    win32api.keybd_event(ord('V'), 0, 0, 0);
    win32api.keybd_event(ord('V'), 0, win32con.KEYEVENTF_KEYUP, 0);
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0);

# AT a name.
def QQ_AtPerson(name):
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0);
    win32api.keybd_event(ord('2'), 0, 0, 0);
    win32api.keybd_event(ord('2'), 0, win32con.KEYEVENTF_KEYUP, 0);
    win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0);

    time.sleep(0.5)

    QQ_PrintText(user_list[name]['spell'])

    time.sleep(0.8)

    win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0);
    win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0);

# Parse out the AT directives.
def QQ_parseText(str):
    pos = str.find('@')
    if pos == -1:
        return [str]

    for name in user_list.keys():
        if str.startswith('@' + user_list[name]['name'], pos):
            return [str[:pos]] + [str[pos:pos + 1 + len(user_list[name]['name'])]] + QQ_parseText(str[pos + 1 + len(user_list[name]['name']):])

def QQ_PrintTextWithAt(str):
    phrase_list = QQ_parseText(str)
    temp_list = []
    for phrase in phrase_list:
        if phrase != '':
            temp_list.append(phrase)
    phrase_list = temp_list

    print 'Sending: ',
    for phrase in phrase_list:
        print '"' + phrase + '",',

    # Populate the textbox of QQ.
    for phrase in phrase_list:
        if phrase.startswith('@'):
            QQ_AtPerson(phrase[1:])
        else:
            QQ_PrintText(phrase)

# Press the "Enter' key.
def QQ_Enter():
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0);
    win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0);
    win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0);
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0);

# The interface function to send QQ a message.
def QQ_SendTextWithAt(str):
    os.system(qq_shortcut)

    try_time = 0
    while True:
        time.sleep(0.5)
        hwnd = win32gui.FindWindow(None, '操作系统&虚拟化小组')
        # hwnd = win32gui.FindWindow(None, 'OSVT小O测试群')
        print('try_time = %d, hwnd = %d' % (try_time, hwnd))
        if hwnd != 0:
            break
        elif try_time >= 60:
            print ('SendTextToQQ Error.')
            return
        else:
            try_time = try_time + 1

    win32gui.SetForegroundWindow(hwnd)

    QQ_PrintTextWithAt(str)
    QQ_Enter()

    # win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    # win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
    # win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, ord('v'), 0)
    # win32gui.PostMessage(hwnd, win32con.WM_KEYUP, ord('v'), 0)


    #win32gui.SendMessage(hwnd, win32con.WM_SETTEXT, None, 'aaa')
    #win32gui.SetWindowText(hwnd, 'aaa')
    #win32gui.ReplaceSel()
    #win32gui.PostMessage(hwnd, win32con.WM_CHAR, '他', 3)

    # win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_CONTROL, 0)
    # win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, ord('V'), 0)
    # win32gui.PostMessage(hwnd, win32con.WM_KEYUP, ord('V'), 0)
    # win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_CONTROL, 0)

if __name__ == '__main__':
    QQ_SendTextWithAt(u'大家好，我是@ly，请多指教！')
