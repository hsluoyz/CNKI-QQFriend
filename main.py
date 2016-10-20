# coding=gbk

import qq
import downloader
import copy_paste

def do_check_request():
    document_name = qq.do_get_document_name()
    if document_name == "":
        # no window poped up
        return

    print "*********************************************"
    print "new request = " + document_name.decode('gbk')
    file_name = downloader.do_download(document_name)
    if file_name == "":
        print "do_check_request::downloader.do_download() fails, file_name = NULL"
        qq.do_close_session()
        return

    copy_paste.copy_file_to_clipboard(file_name)
    qq.do_send_document()
    qq.do_close_session()

if __name__ == '__main__':
    do_check_request()