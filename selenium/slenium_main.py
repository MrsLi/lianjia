# coding=utf-8
from selenium import webdriver

browser = webdriver.Chrome()
browser.get("https://sh.lianjia.com/zufang")
input_third = browser.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[1]/div[1]/p[1]/a/text()')
#print(browser.page_source)
print(input_third)
