from selenium import webdriver

browser = webdriver.PhantomJS()

browser.get('http://www.google.com')
browser.quit()