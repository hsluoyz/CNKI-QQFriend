# coding=gbk

import qq
import downloader
import web
import copy_paste

import time
from apscheduler.schedulers.blocking import BlockingScheduler

def do_check_request():
    document_name = qq.do_get_document_name()
    if document_name == "":
        # no window poped up.
        return

    document_name = downloader.is_document_title(document_name)
    if document_name == "":
        # not a document request.
        qq.do_close_session()
        return

    print "*********************************************"
    print "new request = " + document_name.decode('gbk')
    file_name = web.do_download(document_name)
    if file_name == "":
        print "do_check_request::downloader.do_download() fails, file_name = NULL"
        qq.QQ_PrintText("No document found!")
        time.sleep(0.5)
        qq.QQ_Enter()
        time.sleep(0.5)
        qq.do_close_session()
        return

    copy_paste.copy_file_to_clipboard(file_name)
    qq.do_send_document()
    qq.do_close_session()

def do_check_request_dummy():
    print "Test request"

if __name__ == '__main__':
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    print time.strftime(ISOTIMEFORMAT, time.localtime())

    do_check_request()

    scheduler = BlockingScheduler()
    scheduler.add_job(do_check_request, 'cron', second='*/3')

    print('Press Ctrl+Break to exit')

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
