import time


def login(browser, sample_user_email, sample_user_password):
    signin_btn = browser.find_element_by_xpath('//a[@href="#/login"]')
    signin_btn.click()
    email_input = browser.find_element_by_xpath('//input[@type="text"]')
    password_input = browser.find_element_by_xpath('//input[@type="password"]')
    login_btn = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    email_input.send_keys(sample_user_email)
    password_input.send_keys(sample_user_password)
    login_btn.click()


def new_article(browser, title_input, about_input, main_input, tag_input):
    new_article_btn = browser.find_elements_by_css_selector('a[class="nav-link"]')[0]
    new_article_btn.click()
    time.sleep(2)
    sample_article_title = browser.find_element_by_css_selector('input[class="form-control form-control-lg"]')
    sample_article_title.send_keys(title_input)
    sample_article_about = browser.find_element_by_xpath('//input[@class="form-control"]')
    sample_article_about.send_keys(about_input)
    sample_article_main = browser.find_element_by_css_selector('textarea[class="form-control"]')
    sample_article_main.send_keys(main_input)
    sample_article_tag = browser.find_element_by_xpath('//input[@placeholder="Enter tags"]')
    sample_article_tag.send_keys(tag_input)
    publish_article_btn = browser.find_element_by_xpath('//button[@class="btn btn-lg pull-xs-right btn-primary"]')
    publish_article_btn.click()