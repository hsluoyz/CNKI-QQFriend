# coding=gbk

import splinter
import time


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
    browser = splinter.Browser('chrome')
    browser.visit('http://www.niuniulib.com/e/member/login/')

    input_box_username = browser.find_by_id('username')
    input_box_username.fill('6007544018')

    input_box_password = browser.find_by_id('password')
    input_box_password.fill('415344')

    # browser.choose('lifetime', '3600')

    search_btn = browser.find_by_name('Submit')
    search_btn.click()

    # browser.is_text_present('登录成功'.decode('gbk'), wait_time=10)
    time.sleep(5)

    mainpage_link = browser.find_by_xpath('/html/body/div[2]/div[2]/div[4]/a[1]')
    mainpage_link.click()

    chineselib_link = browser.find_by_xpath('//*[@id="content"]/div[1]/div[2]/dl[1]/dt/a')
    chineselib_link.click()

    # browser.visit('http://www.niuniulib.com/zhongwenku/')

    recommended_link = browser.find_by_xpath('//*[@id="maincolumn"]/div[2]/div[2]/span[' + str(entrance_no) + ']/a')
    recommended_link.click()

    new_window = browser.driver.window_handles[1]
    browser.driver.close()
    browser.driver.switch_to.window(new_window)

    time.sleep(5)

    input_box = browser.find_by_id('txt_1_value1')
    input_box.fill(document_title.decode('gbk'))

    search_btn = browser.find_by_id('btnSearch')
    search_btn.click()

    browser.driver.switch_to_frame("iframeResult")

    try_time = 0
    while True:
        first_link = browser.find_by_xpath('//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/a')
        try:
            first_link.click()
            break
        except AttributeError, e:
            print AttributeError, ": ", e
            print "download_from_niuniu::first_link.click() failed, try_time = " + str(try_time)
            if try_time > 3:
                print "download_from_niuniu::first_link.click() failed, too many attempts, abort."
                browser.quit()
                return False
            else:
                try_time += 1
                browser.reload()

    # browser = splinter.Browser('chrome')
    # browser.visit('http://www.cnki.net/KCMS/detail/detail.aspx?QueryID=0&CurRec=1&recid=&filename=JXCY201401007&dbname=CJFD2014&dbcode=CJFQ&pr=&urlid=&yx=&v=MTYyODdTN0RoMVQzcVRyV00xRnJDVVJMeWVaK1JxRnk3bFZiclBMelhJZDdHNEg5WE1ybzlGWTRSOGVYMUx1eFk=')

    detail_window = browser.driver.window_handles[1]
    browser.driver.close()
    browser.driver.switch_to.window(detail_window)

    pdf_link = browser.find_by_xpath('//*[@id="QK_nav"]/ul/li[2]/a')
    try:
        pdf_link.click()
    except AttributeError, e:
        print AttributeError, ": ", e
        print "download_from_niuniu::pdf_link.click() failed."
        browser.quit()
        return False

    time.sleep(5)
    print "download succeed, document_title = " + document_title.decode('gbk')
    browser.quit()
    return True


if __name__ == '__main__':
    # download_document('计算机')
    download_from_niuniu('中德两国高中生数学能力的分析及比较', 4)
