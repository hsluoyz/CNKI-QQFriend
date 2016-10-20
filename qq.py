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

def QQ_OpenActiveWindow():
    window_name = u'OSVT助理小O'
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd == 0:
        return False
    print "find window = " + window_name
    win32gui.SetForegroundWindow(hwnd)
    return True

# Press the "Alt + H' key.
def QQ_ToggleMessageRecord():
    win32api.keybd_event(win32con.VK_MENU, 0, 0, 0);
    win32api.keybd_event(ord('H'), 0, 0, 0);
    win32api.keybd_event(ord('H'), 0, win32con.KEYEVENTF_KEYUP, 0);
    win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0);

# Copy the last message.
def QQ_CopyText():
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0);
    win32api.keybd_event(ord('C'), 0, 0, 0);
    win32api.keybd_event(ord('C'), 0, win32con.KEYEVENTF_KEYUP, 0);
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0);

# Close the window.
def QQ_CloseWindow():
    win32api.keybd_event(win32con.VK_MENU, 0, 0, 0);
    win32api.keybd_event(win32con.VK_F4, 0, 0, 0);
    win32api.keybd_event(win32con.VK_F4, 0, win32con.KEYEVENTF_KEYUP, 0);
    win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0);

# Get the clipboard into a str.
def QQ_GetClipboardText():
    win32clipboard.OpenClipboard()
    try:
        message_text = win32clipboard.GetClipboardData(win32con.CF_TEXT)
    except Exception, e:
        print "win32clipboard.GetClipboardData() failed"
        print Exception, ": ", e
        win32clipboard.CloseClipboard()
        return ""
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()
    return message_text

def QQ_GetMessageRecordText():
    try_time = 0
    while True:
        QQ_CopyText()
        time.sleep(0.5)

        message_text = QQ_GetClipboardText()
        print('try_time = %d, message_text = %s' % (try_time, message_text.decode('gbk')))
        if message_text != "":
            break
        elif try_time >= 10:
            print ('QQ_GetClipboardText Error.')
            return ""
        else:
            try_time += 1
    return message_text

def getDocumentName(message_text):
    print "received message = \n" + message_text.decode('gbk')
    tmp_list = message_text.split('\r\n')
    title = tmp_list[1]
    print "document title = " + title.decode('gbk')
    return title

# Paste the file.
def QQ_PasteFile():
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0);
    win32api.keybd_event(ord('V'), 0, 0, 0);
    win32api.keybd_event(ord('V'), 0, win32con.KEYEVENTF_KEYUP, 0);
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0);

def QQ_SendOffline():
    QQ_Enter()
    time.sleep(0.2)
    for i in range(0, 10):
        print "tab = " + str(i)
        win32api.keybd_event(win32con.VK_TAB, 0, 0, 0);
        win32api.keybd_event(win32con.VK_TAB, 0, win32con.KEYEVENTF_KEYUP, 0);
        time.sleep(0.2)
    QQ_Enter()

def do_get_document_name():
    if QQ_OpenActiveWindow():
        time.sleep(1.0)
        QQ_ToggleMessageRecord()
        time.sleep(1.0)

        message_text = QQ_GetMessageRecordText()
        QQ_ToggleMessageRecord()
        return getDocumentName(message_text)
    else:
        return ""

def do_send_document():
    if QQ_OpenActiveWindow():
        time.sleep(1.0)
        QQ_PasteFile()
        QQ_SendOffline()
    else:
        print "do_send_document() error, not sending document!"

def do_close_session():
    print "close the current session."
    QQ_CloseWindow()

if __name__ == '__main__':
    # do_get_document_name()

    # message_text = u"OSVT助理小O 12:26:54 AM\n中德两国高中生数学能力的分析及比较\n\n"
    # getDocumentName(message_text)

    do_send_document()

    ## QQ_SendTextWithAt(u'大家好，我是@ly，请多指教！')
