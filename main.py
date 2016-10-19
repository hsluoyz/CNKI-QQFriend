# coding=gbk

import qq
import downloader

def do_check_request():
    document_name = qq.do_get_document_name()
    if document_name == "":
        return

    print "*********************************************"
    print "new request = " + document_name
    downloader.do_download(document_name)
    qq.do_send_document()
    qq.do_close_session()

if __name__ == '__main__':
    do_check_request()