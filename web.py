# coding=gbk

import splinter


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

if __name__ == '__main__':
    download_document('计算机')
