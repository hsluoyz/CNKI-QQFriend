# coding=gbk

import splinter
import time
import selenium
import os
import shutil

document_folder = os.path.abspath('.') + '\output'


def download_document(document_title):
    browser = splinter.Browser('chrome')
    browser.visit('http://www.cnki.net/')

    input_box = browser.find_by_id('txt_1_value1')
    input_box.fill(document_title.decode('gbk'))

    search_btn = browser.find_by_id('btnSearch')
    search_btn.click()

    # browser.find_by_css("body")

    browser.driver.switch_to_frame("iframeResult")
    first_link = browser.find_by_xpath('//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/a')
    first_link.click()

    # browser = splinter.Browser('chrome')
    # browser.visit('http://www.cnki.net/KCMS/detail/detail.aspx?QueryID=0&CurRec=1&recid=&filename=JXCY201401007&dbname=CJFD2014&dbcode=CJFQ&pr=&urlid=&yx=&v=MTYyODdTN0RoMVQzcVRyV00xRnJDVVJMeWVaK1JxRnk3bFZiclBMelhJZDdHNEg5WE1ybzlGWTRSOGVYMUx1eFk=')

    detail_window = browser.driver.window_handles[1]
    browser.driver.close()
    browser.driver.switch_to.window(detail_window)

    pdf_link = browser.find_by_xpath('//*[@id="QK_nav"]/ul/li[2]/a')
    pdf_link.click()

    # browser.find_link_by_text(u"PDF下载")
    # browser.driver.quit()


def download_from_niuniu(document_title, entrance_no):
    options = selenium.webdriver.ChromeOptions()
    prefs = {'download.default_directory': document_folder}
    options.add_experimental_option("prefs", prefs)
    # options.add_argument('intl.charset_default=GBK')
    # options.add_argument('start-maximized')
    options.add_argument('lang=zh-CN')
    # options.add_argument('download.default_directory=' + os.path.abspath('.') + '\output')

    # dc = options.to_capabilities()
    # browser = splinter.Browser('chrome', desired_capabilities=dc)

    print 'go to the login page'
    browser = splinter.Browser('chrome', options=options)
    browser.visit('http://www.niuniulib.com/e/member/login/')

    print 'input username..'
    input_box_username = browser.find_by_id('username')
    input_box_username.fill('6007544018')

    print 'input password..'
    input_box_password = browser.find_by_id('password')
    input_box_password.fill('415344')

    # browser.choose('lifetime', '3600')

    print 'click "Submit"'
    search_btn = browser.find_by_name('Submit')
    search_btn.click()

    # browser.is_text_present('登录成功'.decode('gbk'), wait_time=10)
    # print 'sleep 5 seconds..'
    # time.sleep(5)

    if '如果您的浏览器没有自动跳转，请点击这里'.decode('gbk') in browser.html:
        print "found the success page, do the jump"
        jump_link = browser.find_by_xpath('/html/body/table/tbody/tr[2]/td/div/a')
        jump_link.click()

    print 'go to the main page'
    mainpage_link = browser.find_by_xpath('/html/body/div[2]/div[2]/div[4]/a[1]')
    mainpage_link.click()

    print 'go to the Chinese library page'
    chineselib_link = browser.find_by_xpath('//*[@id="content"]/div[1]/div[2]/dl[1]/dt/a')
    chineselib_link.click()

    # browser.visit('http://www.niuniulib.com/zhongwenku/')

    print 'go to one of the recommended entrances'
    recommended_link = browser.find_by_xpath('//*[@id="maincolumn"]/div[2]/div[2]/span[' + str(entrance_no) + ']/a')
    recommended_link.click()

    new_window = browser.driver.window_handles[-1]
    browser.driver.close()
    browser.driver.switch_to.window(new_window)

    print 'sleep 5 seconds..'
    time.sleep(5)

    try_time = 0
    while True:
        try:
            print 'input the title: ' + document_title.decode('gbk')
            input_box = browser.find_by_id('txt_1_value1')
            input_box.fill(document_title.decode('gbk'))
            break
        except AttributeError, e:
            print AttributeError, ": ", e
            print "download_from_niuniu::input_box.fill() failed, try_time = " + str(try_time)
            if try_time > 5:
                print "download_from_niuniu::input_box.fill() failed, too many attempts, abort."
                browser.quit()
                return ''
            else:
                try_time += 1
                time.sleep(3)

    print 'click "Search"'
    search_btn = browser.find_by_id('btnSearch')
    search_btn.click()

    browser.driver.switch_to_frame("iframeResult")

    try_time = 0
    while True:
        first_link = browser.find_by_xpath('//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/a')
        try:
            print 'try to click the first article..'
            first_link.click()
            break
        except AttributeError, e:
            print AttributeError, ": ", e
            print "download_from_niuniu::first_link.click() failed, try_time = " + str(try_time)
            if try_time > 3:
                print "download_from_niuniu::first_link.click() failed, too many attempts, abort."
                browser.quit()
                return ''
            else:
                try_time += 1
                browser.reload()

    # browser = splinter.Browser('chrome')
    # browser.visit('http://www.cnki.net/KCMS/detail/detail.aspx?QueryID=0&CurRec=1&recid=&filename=JXCY201401007&dbname=CJFD2014&dbcode=CJFQ&pr=&urlid=&yx=&v=MTYyODdTN0RoMVQzcVRyV00xRnJDVVJMeWVaK1JxRnk3bFZiclBMelhJZDdHNEg5WE1ybzlGWTRSOGVYMUx1eFk=')

    detail_window = browser.driver.window_handles[-1]
    browser.driver.close()
    browser.driver.switch_to.window(detail_window)

    pdf_link = browser.find_by_xpath('//*[@id="QK_nav"]/ul/li[2]/a')
    try:
        print 'try to download the article as PDF..'
        pdf_link.click()
    except AttributeError, e:
        print AttributeError, ": ", e
        print "download_from_niuniu::pdf_link.click() failed, maybe it's a CAJ file."

    caj_link = browser.find_by_xpath('//*[@id="nav"]/ul/li[3]/a')
    try:
        print 'try to download the article as CAJ..'
        caj_link.click()
    except AttributeError, e:
        print AttributeError, ": ", e
        print "download_from_niuniu::caj_link.click() failed."
        browser.quit()
        return ''

    print 'sleep 5 seconds..'
    time.sleep(5)

    try:
        alert = browser.get_alert()
        print "alert text = " + alert.text
        if '并发数'.decode('gbk') in alert.text:
            print "download failed, too many people are downloading documents. Abort."
            alert.accept()
            browser.quit()
            return ''
    except selenium.common.exceptions.NoAlertPresentException, e:
        # print selenium.common.exceptions.NoAlertPresentException, ": ", e
        print "No alert window, good! go on.."

    if '对不起，您的下载请求不合法'.decode('gbk') in browser.html:
        print "download failed, the download request is illegal. Abort."
        browser.quit()
        return ''

    document_file = is_document_downloaded()
    if document_file != '':
        print "download succeed, document_title = " + document_title.decode('gbk')
    else:
        print "download_from_niuniu failed, no file generated."
    browser.quit()
    return document_file

    # download_url = pdf_link['href']
    # print "download_url = " + download_url.decode('gbk')
    # import requests
    #
    # cookies = {browser.cookies.all()[0]["name"]: browser.cookies.all()[0]["value"]}
    # result = requests.get(download_url, cookies=cookies)
    # print "download succeed, document_title = " + document_title.decode('gbk')
    #
    # pdf = open("C:/111.pdf", 'w')
    # pdf.write(result.content)
    # pdf.close()
    # print "document generated, path = " + "C:/111.pdf"
    #
    # browser.quit()
    # return True


def do_delete():
    if os.path.exists(document_folder):
        print "delete folder = " + document_folder.decode('gbk')
        shutil.rmtree(document_folder)
    else:
        print "folder doesn't exist, no need to delete, folder = " + document_folder.decode('gbk')


def is_document_downloaded():
    if not os.path.exists(document_folder):
        print "folder doesn't exist, the download should have failed, abort."
        return ""

    try_time = 0
    previous_file_size = 0
    while True:
        has_file = False
        for file in os.listdir(document_folder):
            has_file = True
            print "found file = " + file.decode('gbk')
            if file.endswith('.crdownload'):
                file_size = os.path.getsize(document_folder + '/' + file) / 1024
                if previous_file_size != file_size:
                    print "downloaded = %d KBytes.." % (file_size)
                    previous_file_size = file_size
                    time.sleep(5)
                else:
                    print "downloaded = %d KBytes, no progress, try_time = %d" % (file_size, try_time)
                    if try_time < 15:
                        print "wait for 5 seconds to try again.."
                        try_time += 1
                        time.sleep(5)
                    else:
                        print "already tried 5 times, abort."
                        return ""
            elif file.endswith('.pdf') or file.endswith('.caj'):
                print "download complete."
                return str(file)
            else:
                print "strange file found, filename = " + file.decode('gbk')
                return ""
        if not has_file:
            print "download is not started, abort."
            return ""


def do_download(document_name):
    # Try to download the document for several times.
    for i in range(0, 3, 1):
        print "do_download::download_from_niuniu() is excuting, try_time = " + str(i)
        do_delete()
        filename = download_from_niuniu(document_name, 4)
        if filename == '':
            print "do_download::download_from_niuniu() fails, download fails! (maybe try again)"
        else:
            # download succeed
            print "do_download::download_from_niuniu() succeeds!"
            break
    if filename == '':
        print "do_download::download_from_niuniu() fails, download fails 3 times, abort."
        return ""

    return filename


def test_alert():
    browser = splinter.Browser('chrome')
    browser.visit('file:///C:/Users/Administrator/Desktop/pop.htm')

    search_btn = browser.find_by_xpath('/html/body/p[7]/input')
    search_btn.click()

    time.sleep(2)
    alert = browser.get_alert()
    print "alert text = " + alert.text
    if '我敢保证'.decode('gbk') in alert.text:
        print "download failed, too many people are downloading documents. Abort."
    alert.accept()


def test_check_string():
    browser = splinter.Browser('chrome')
    browser.visit('file:///C:/Users/Administrator/Desktop/docdownload.cnki.net.html')
    if '对不起，您的下载请求不合法'.decode('gbk') in browser.html:
        print "found"


def test_check_logon():
    browser = splinter.Browser('chrome')
    browser.visit('file:///C:/Users/Administrator/Desktop/%E7%89%9B%E7%89%9B%E5%9B%BE%E4%B9%A6%E9%A6%86%E6%8F%90%E7%A4%BA.html')
    if '如果您的浏览器没有自动跳转，请点击这里'.decode('gbk') in browser.html:
        print "found"
        search_btn = browser.find_by_xpath('/html/body/table/tbody/tr[2]/td/div/a')
        search_btn.click()


if __name__ == '__main__':
    # download_document('计算机')
    # download_from_niuniu('中德两国高中生数学能力的分析及比较', 4)
    # do_delete()
    # is_document_downloaded()
    do_download('中德两国高中生数学能力的分析及比较')
    # test_check_string()
    # test_check_logon()
