# coding=gbk

import splinter
import time
import selenium
import os
import shutil
import captcha

document_folder = os.path.abspath('.') + '\output'
captcha_folder = os.path.abspath('.') + '\\captcha\\'


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

    # print 'sleep 5 seconds..'
    # time.sleep(5)

    if entrance_no == 3:
        try_time = 0
        while True:
            try:
                print "try to log on again.."
                logon_link = browser.find_by_xpath('//*[@id="maincolumn"]/div[1]/div[2]/table/tbody/tr/td/a[1]')
                logon_link.click()
                break
            except AttributeError, e:
                print AttributeError, ": ", e
                print "download_from_niuniu::logon_link.click() failed, try_time = " + str(try_time)
                if try_time > 5:
                    print "download_from_niuniu::logon_link.click() failed, too many attempts, abort."
                    browser.quit()
                    return ''
                else:
                    try_time += 1
                    time.sleep(3)

        print 'input username..'
        input_box_username = browser.find_by_id('username')
        input_box_username.fill('6007544018')

        print 'input password..'
        input_box_password = browser.find_by_id('password')
        input_box_password.fill('415344')

        print 'click "Submit"'
        search_btn = browser.find_by_name('Submit')
        search_btn.click()

        if '如果您的浏览器没有自动跳转，请点击这里'.decode('gbk') in browser.html:
            print "found the success page, do the jump"
            jump_link = browser.find_by_xpath('/html/body/table/tbody/tr[2]/td/div/a')
            jump_link.click()
    elif entrance_no == 5:
        try_time = 0
        try_time_max = 50
        while True:
            captcha.do_delete()
            os.mkdir(captcha_folder)
            print "try to recognize the captcha.."
            captcha_img = browser.find_by_xpath('//*[@id="regimg"]')
            captcha_img = captcha_img[0]

            get_captcha(browser.driver, captcha_img, captcha_folder)
            captcha.preprocess('captcha.bmp', 'captcha_output.bmp')
            captcha_word = captcha.solve('captcha_output.bmp')
            if captcha_word == '':
                if try_time < try_time_max:
                    print "download_from_niuniu::captcha.solve() failed, try_time = " + str(try_time)
                    try_time += 1

                    print "refresh the captcha"
                    # refresh_captcha_link = browser.find_by_xpath('//*[@id="loginHtml"]/a[1]')
                    # '//*[@id="loginHtml"]/a[1]'
                    # refresh_captcha_link.click()
                    browser.reload()
                    continue
                else:
                    print "download_from_niuniu::captcha.solve() failed, too many attempts, abort."
                    browser.quit()
                    return ''

            print 'input captcha..'
            input_box_captcha = browser.find_by_xpath('//*[@id="loginHtml"]/input[1]')
            try:
                input_box_captcha.fill(captcha_word)
            except UnicodeDecodeError, e:
                print UnicodeDecodeError, ": ", e
                print "download_from_niuniu::input_box_captcha.fill() failed, try_time = " + str(try_time)
                if try_time > try_time_max:
                    print "download_from_niuniu::input_box_captcha.fill() failed, too many attempts, abort."
                    browser.quit()
                    return ''
                else:
                    try_time += 1
                    browser.reload()
                    continue

            print 'click "Submit"'
            submit_btn = browser.find_by_xpath('//*[@id="loginHtml"]/input[2]')
            submit_btn.click()

            if '登录失败'.decode('gbk') in browser.html or '验证码不正确，不能登录'.decode('gbk') in browser.html:
                if try_time < try_time_max:
                    print "the captcha is wrong, can't log in, try_time = " + str(try_time)
                    try_time += 1

                    back_btn = browser.find_by_xpath('/html/body/table[5]/tbody/tr/td[2]/table[3]/tbody/tr/td/input')
                    back_btn.click()

                    print "refresh the captcha"
                    # refresh_captcha_link = browser.find_by_xpath('//*[@id="loginHtml"]/a[1]')
                    # '//*[@id="loginHtml"]/a[1]'
                    # refresh_captcha_link.click()
                    browser.reload()
                    continue
                else:
                    print "the captcha is wrong, can't log in, too many attempts, abort."
                    browser.quit()
                    return ''
            else:
                print 'the captcha passed.'
                break

    try_time = 0
    while True:
        try:
            print 'try to input the title: ' + document_title.decode('gbk')
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
        try:
            print 'try to click the first article..'
            first_link = browser.find_by_xpath('//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/a')
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
                # browser.reload()

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

    # if len(browser.driver.window_handles) >= 2:
    #     print "there are %d windows, switch to the last one" % (len(browser.driver.window_handles))
    #     download_window = browser.driver.window_handles[-1]
    #     # browser.driver.close()
    #     browser.driver.switch_to.window(download_window)

    print 'sleep 8 seconds..'
    time.sleep(8)

    # try:
    #     # browser.driver.switch_to_alert()
    #     alert = browser.get_alert()
    #     print "alert text:"
    #     print alert.text
    #     # if '并发数'.decode('gbk') in alert.text:
    #     print "download failed, too many people are downloading documents. Abort."
    #     alert.accept()
    #     browser.quit()
    #     return ''
    # except selenium.common.exceptions.NoAlertPresentException, e:
    #     print selenium.common.exceptions.NoAlertPresentException, ": ", e
    #     print "No alert window, good! go on.."
    #
    # if '对不起，您的下载请求不合法'.decode('gbk') in browser.html:
    #     print "download failed, the download request is illegal. Abort."
    #     browser.quit()
    #     return ''

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
                if previous_file_size < file_size:
                    print "downloaded = %d KBytes.." % (file_size)
                    previous_file_size = file_size
                    try_time = 0
                    time.sleep(2)
                else:
                    print "downloaded = %d KBytes, no progress, try_time = %d" % (file_size, try_time)
                    if try_time < 20:
                        print "wait for 2 seconds to try again.."
                        try_time += 1
                        time.sleep(2)
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
    entrances = [5, 4, 3, 7]
    for i in range(0, len(entrances)):
        print "do_download::download_from_niuniu() is excuting, entrance = " + str(entrances[i]) + ", try_time = " + str(i)
        do_delete()
        filename = download_from_niuniu(document_name, entrances[i])
        if filename == '':
            print "do_download::download_from_niuniu() fails, download fails! (maybe try again)"
        else:
            # download succeed
            print "do_download::download_from_niuniu() succeeds!"
            break
    if filename == '':
        print "do_download::download_from_niuniu() fails, download fails %d times, abort." % (len(entrances))
        return ""

    return filename


def test_alert():
    browser = splinter.Browser('chrome')
    browser.visit('file:///C:/Users/Administrator/Desktop/pop.htm')

    search_btn = browser.find_by_xpath('/html/body/p[7]/input')
    search_btn.click()

    time.sleep(2)
    try:
        alert = browser.get_alert()
        print "alert text = " + alert.text
        if '我敢保证'.decode('gbk') in alert.text:
            print "found."
        else:
            print "not found."
        alert.accept()
    except selenium.common.exceptions.NoAlertPresentException, e:
        print selenium.common.exceptions.NoAlertPresentException, ": ", e
        print "No alert window, good! go on.."


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


def get_captcha(driver, element, folder):
    from PIL import Image

    # saves screenshot of entire page
    driver.save_screenshot(folder + 'screenshot.bmp')
    print "saved screenshot = " + folder + 'screenshot.bmp'
    # time.sleep(3)

    # uses PIL library to open image in memory
    image = Image.open(folder + 'screenshot.bmp')

    left = int(element['x'])
    top = int(element['y'])
    right = left + int(element['width'])
    bottom = top + int(element['height'])
    print 'image location & size = (%d, %d) -> (%d, %d)' % (left, top, right, bottom)
    image = image.crop((left, top, right, bottom))  # defines crop points
    image.save(folder + 'captcha.bmp', 'bmp')  # saves new cropped image
    print "retrieved captcha = " + folder + 'captcha.bmp'


def test_captcha():
    browser = splinter.Browser('chrome')
    browser.visit('http://www.niuniulib.com/e/action/ShowInfo.php?classid=1&id=953')

    try_time = 0
    while True:
        try:
            print "try to log on again.."
            logon_link = browser.find_by_xpath('//*[@id="maincolumn"]/div[1]/div[2]/table/tbody/tr/td/a[1]')
            logon_link.click()
            break
        except AttributeError, e:
            print AttributeError, ": ", e
            print "download_from_niuniu::logon_link.click() failed, try_time = " + str(try_time)
            if try_time > 5:
                print "download_from_niuniu::logon_link.click() failed, too many attempts, abort."
                browser.quit()
                return ''
            else:
                try_time += 1
                time.sleep(3)

    print 'input username..'
    input_box_username = browser.find_by_id('username')
    input_box_username.fill('6007544018')

    print 'input password..'
    input_box_password = browser.find_by_id('password')
    input_box_password.fill('415344')

    print 'click "Submit"'
    search_btn = browser.find_by_name('Submit')
    search_btn.click()

    if '如果您的浏览器没有自动跳转，请点击这里'.decode('gbk') in browser.html:
        print "found the success page, do the jump"
        jump_link = browser.find_by_xpath('/html/body/table/tbody/tr[2]/td/div/a')
        jump_link.click()

    try_time = 0
    try_time_max = 50
    while True:
        captcha.do_delete()
        os.mkdir(captcha_folder)
        print "try to recognize the captcha.."
        captcha_img = browser.find_by_xpath('//*[@id="regimg"]')
        captcha_img = captcha_img[0]

        get_captcha(browser.driver, captcha_img, captcha_folder)
        captcha.preprocess('captcha.bmp', 'captcha_output.bmp')
        captcha_word = captcha.solve('captcha_output.bmp')
        if captcha_word == '':
            if try_time < try_time_max:
                print "download_from_niuniu::captcha.solve() failed, try_time = " + str(try_time)
                try_time += 1

                print "refresh the captcha"
                # refresh_captcha_link = browser.find_by_xpath('//*[@id="loginHtml"]/a[1]')
                # '//*[@id="loginHtml"]/a[1]'
                # refresh_captcha_link.click()
                browser.reload()
                continue
            else:
                print "download_from_niuniu::captcha.solve() failed, too many attempts, abort."
                browser.quit()
                return ''

        print 'input captcha..'
        input_box_captcha = browser.find_by_xpath('//*[@id="loginHtml"]/input[1]')
        try:
            input_box_captcha.fill(captcha_word)
        except UnicodeDecodeError, e:
            print UnicodeDecodeError, ": ", e
            print "download_from_niuniu::input_box_captcha.fill() failed, try_time = " + str(try_time)
            if try_time > try_time_max:
                print "download_from_niuniu::input_box_captcha.fill() failed, too many attempts, abort."
                browser.quit()
                return ''
            else:
                try_time += 1
                browser.reload()
                continue

        print 'click "Submit"'
        submit_btn = browser.find_by_xpath('//*[@id="loginHtml"]/input[2]')
        submit_btn.click()

        if '登录失败'.decode('gbk') in browser.html or '验证码不正确，不能登录'.decode('gbk') in browser.html:
            if try_time < try_time_max:
                print "the captcha is wrong, can't log in, try_time = " + str(try_time)
                try_time += 1

                back_btn = browser.find_by_xpath('/html/body/table[5]/tbody/tr/td[2]/table[3]/tbody/tr/td/input')
                back_btn.click()

                print "refresh the captcha"
                # refresh_captcha_link = browser.find_by_xpath('//*[@id="loginHtml"]/a[1]')
                # '//*[@id="loginHtml"]/a[1]'
                # refresh_captcha_link.click()
                browser.reload()
                continue
            else:
                print "the captcha is wrong, can't log in, too many attempts, abort."
                browser.quit()
                return ''
        else:
            print 'the captcha passed.'
            break


########################################################################################
# No    Name                Owner               Feature                 Supported
# 3:    推荐入口（一）     佛山市图书馆, gz0413  需要登录两次                Yes
# 4:    推荐入口（三）     华东师范大学      类型全，容易并发数过多           Yes
# 5:    推荐入口（二）     gz0225            类型全，需要验证码              Yes
# 7:    推荐入口（四）     mfshw               没有订阅硕博士                Yes
# 15:   知网(华东师范)     华东师范大学      类型全，容易并发数过多           Yes


if __name__ == '__main__':
    # download_document('计算机')
    # do_delete()
    download_from_niuniu('数学', 5)
    # do_delete()
    # is_document_downloaded()
    # do_download('中德两国高中生数学能力的分析及比较')
    # test_alert()
    # test_check_string()
    # test_check_logon()
    # test_captcha()
