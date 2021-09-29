
import pandas as pd
from selenium import webdriver
import time
import re
import pdfkit

# 从本地读入所需cik和year
cik_fyear = pd.read_csv('C:\\Users\\39081\\Desktop\\CUHK\\code\\cik_fyear.csv')
tickerCode = cik_fyear['cik']
tickerCode = tickerCode.values.tolist()
a = cik_fyear.iloc[0]
print(a)
year = a[0]
cik = a[1]
print("year=%d"%year)
print("cik=%d"%cik)
print("-------------------------分割线-------------------------")\

def url_to_pdf(url, to_file):
    # 将wkhtmltopdf.exe程序绝对路径传入config对象
    path_wkthmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    # 生成pdf文件，to_file为文件路径
    pdfkit.from_url(url, to_file, configuration=config)
    print('完成')


for i in range(0, 4850):
    trans = cik_fyear.iloc[i]
    year = trans[0]
    cik = trans[1]
    pdfName = str(cik) + "_10-K_" + str(year) + ".pdf"
    print("year=%d, cik=%d"%(year, cik))
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(options=options)
    url = "https://www.sec.gov/edgar/browse/?CIK=" + str(cik) + "&owner=exclude"
    print(url)
    browser.get(url)
    pathRoot = "//div[@id='filings']//tbody//tr//td[text()='10-K']/..//*[@class='sorting_1']/../*[contains(text(),'" + str(year) + "')]/..//*[@class='document-link']"
    print(pathRoot)
    # 通过两次模拟鼠标点击，进入到dataTables
    browser.find_elements_by_class_name("collapsible")[1].click()
    time.sleep(1)
    browser.find_element_by_xpath("//div//*[@class='btn btn-sm btn-info js-selected-view-all' and @data-group='annualOrQuarterlyReports']").click()
    time.sleep(1)
    browser.find_element_by_xpath("//main//*[contains(text(), 'Search table')]/../input[@id='filingDateFrom']").clear()
    time.sleep(2)
    elements = browser.find_element_by_xpath(pathRoot)
    OuterElement = elements.get_attribute('outerHTML')
    print('OuterElement')
    print(OuterElement)
    findHtml = re.compile(r'href="(.*?)"')
    link = re.findall(findHtml, OuterElement)
    print(link)
    realLink = "https://www.sec.gov" + str(link[0])
    print(realLink)
    browser.get(realLink)
    url_to_pdf(realLink, pdfName)
    browser.quit()
    time.sleep(4)


