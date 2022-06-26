import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from sample_data import sample_user
from sample_functions import login, new_article
from sample_article import article
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import csv


class TestConduit(object):
    def setup(self):
        browser_options = Options()
        browser_options.headless = True
        # options = webdriver.ChromeOptions()
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
        self.browser.get("http://localhost:1667/")

    def teardown(self):
        self.browser.quit()

    # TC001 - Regisztráció - negatív ág

    def test_reg(self):
        signup_btn = self.browser.find_element_by_xpath('//a[@href="#/register"]')
        signup_btn.click()
        username_input = self.browser.find_element_by_xpath('//input[@placeholder="Username"]')
        email_input = self.browser.find_element_by_xpath('//input[@placeholder="Email"]')
        password_input = self.browser.find_element_by_xpath('//input[@type="password"]')
        signup_btn = self.browser.find_element_by_css_selector('button[class="btn btn-lg btn-primary pull-xs-right"]')
        username_input.send_keys('teszt')
        email_input.send_keys('teszt')
        password_input.send_keys('teszt')
        time.sleep(1)
        signup_btn.click()
        time.sleep(1)
        reg_fail = self.browser.find_element_by_xpath('//div[@class="swal-title"]')
        reg_invalid_email = self.browser.find_element_by_xpath('//div[@class="swal-text"]')
        assert reg_fail.text == "Registration failed!"
        assert reg_invalid_email.text == "Email must be a valid email."

    # TC002 - Bejelentkezés - pozitív ág

    def test_logging_in(self):
        signin_btn = self.browser.find_element_by_xpath('//a[@href="#/login"]')
        signin_btn.click()
        email_input = self.browser.find_element_by_xpath('//input[@type="text"]')
        password_input = self.browser.find_element_by_xpath('//input[@type="password"]')
        login_btn = self.browser.find_element_by_css_selector('button[class="btn btn-lg btn-primary pull-xs-right"]')
        email_input.clear()
        password_input.clear()
        email_input.send_keys(sample_user["email"])
        password_input.send_keys(sample_user["password"])
        time.sleep(2)
        login_btn.click()
        time.sleep(2)
        profile = self.browser.find_elements_by_css_selector('a[class="nav-link"]')[2]
        assert profile.text == sample_user["name"]

    # TC003 - Cookie kezelési tájékoztató

    def test_cookies(self):
        accept_btn = self.browser.find_element_by_css_selector(
            'button[class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        accept_btn.click()
        time.sleep(2)
        cookie_panel = self.browser.find_elements_by_xpath(
            '//div[@class="cookie cookie__bar cookie__bar--bottom-left"]')
        assert len(cookie_panel) == 0

    # TC004 - Adatok listázása

    def test_listing_data(self):
        login(self.browser, (sample_user["email"]), (sample_user["password"]))
        time.sleep(1)
        dolor_tag = WebDriverWait(self.browser, 3).until(EC.presence_of_element_located(
            (By.XPATH, '//div[@class="sidebar"]/div[@class="tag-list"]/a[text()="dolor"]')))
        dolor_tag.click()
        time.sleep(2)
        article_list = self.browser.find_elements_by_xpath('//a[@class="preview-link"]/h1')
        assert len(article_list) != 0

    # TC005 - Több oldalas lista bejárása

    def test_pagination(self):
        login(self.browser, (sample_user["email"]), (sample_user["password"]))
        time.sleep(1)
        page_list = self.browser.find_elements_by_xpath('//a[@class="page-link"]')
        for page in page_list:
            page.click()
            active_page = self.browser.find_element_by_xpath('//li[@class="page-item active"]')
            time.sleep(1)
            assert page.text in active_page.text

    # TC006 - Új adat bevitel

    def test_new_article(self):
        login(self.browser, (sample_user["email"]), (sample_user["password"]))
        time.sleep(2)
        new_article(self.browser, article["title"], article["about"], article["main"], article["tag"])
        time.sleep(2)
        article_title = self.browser.find_element_by_xpath('//h1')
        assert article_title.text == article["title"]

    # TC007 - Ismételt és sorozatos adatbevitel adatforrásból

    def test_add_comments(self):
        login(self.browser, (sample_user["email"]), (sample_user["password"]))
        time.sleep(2)
        articles_list = self.browser.find_elements_by_xpath('//a[@class="preview-link"]')
        article_to_comment = articles_list[0]
        article_to_comment.click()
        time.sleep(2)

        comment_field = self.browser.find_element_by_xpath('//textarea[@placeholder="Write a comment..."]')
        post_comment_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-sm btn-primary"]')
        comment_list = self.browser.find_elements_by_xpath('//p[@class="card-text"]')
        with open('test_conduit/comments.csv', 'r', encoding='UTF-8') as file:
            csv_reader = csv.reader(file, delimiter=';')
            for row in csv_reader:
                comment_field.send_keys(row)
                time.sleep(2)
                post_comment_btn.click()

        time.sleep(2)
        comment_list_updated = self.browser.find_elements_by_xpath('//p[@class="card-text"]')
        time.sleep(2)
        assert len(comment_list) == len(comment_list_updated) - 4

    # TC008 - Meglévő adat módosítás

    def test_update_profile_pic(self):
        login(self.browser, (sample_user["email"]), (sample_user["password"]))
        time.sleep(2)
        settings_menu = self.browser.find_element_by_xpath('//a[@href="#/settings"]')
        settings_menu.click()
        time.sleep(2)
        image_input = self.browser.find_element_by_xpath('//input[@placeholder="URL of profile picture"]')
        update_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
        image_input.clear()
        image_input.send_keys("https://cdn.pixabay.com/photo/2020/02/04/16/00/cheetah-4818603_960_720.jpg")
        update_btn.click()
        time.sleep(2)
        result_message = self.browser.find_element_by_xpath('//div[@class="swal-title"]')
        assert result_message.text == "Update successful!"
        confirm_btn = self.browser.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')
        confirm_btn.click()

    # TC009 - Adat vagy adatok törlése

    def test_delete_comment(self):
        login(self.browser, (sample_user["email"]), (sample_user["password"]))
        time.sleep(2)
        articles_list = self.browser.find_elements_by_xpath('//a[@class="preview-link"]')
        article_to_comment = articles_list[0]
        article_to_comment.click()
        time.sleep(2)

        comment_field = self.browser.find_element_by_xpath('//textarea[@placeholder="Write a comment..."]')
        comment_field.send_keys("test comment")
        post_comment_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-sm btn-primary"]')
        post_comment_btn.click()
        time.sleep(2)

        comment_list = self.browser.find_elements_by_xpath('//p[@class="card-text"]')
        delete_btn = self.browser.find_elements_by_xpath('//i[@class="ion-trash-a"]')[0]
        delete_btn.click()
        time.sleep(2)

        comment_list_updated = self.browser.find_elements_by_xpath('//p[@class="card-text"]')
        time.sleep(2)

        assert len(comment_list) == len(comment_list_updated) + 1

    # TC010 - Adatok lementése felületről

    def test_save_data_to_file(self):
        tags = self.browser.find_elements_by_xpath('//a[@class="tag-pill tag-default"]')
        with open('test_conduit/tags.txt', 'w', encoding='UTF-8') as f:
            for tag in tags:
                f.write(tag.text + ', ')
        with open('test_conduit/tags.txt', 'r', encoding='UTF-8') as f:
            txt_tags = f.read().split(', ')
            for i, tag in enumerate(tags):
                assert tag.text == txt_tags[i]

    # TC011 - Kijelentkezés

    def test_logout(self):
        login(self.browser, (sample_user["email"]), (sample_user["password"]))
        time.sleep(1)
        logout_btn = self.browser.find_element_by_xpath('//a[@active-class="active"]')
        logout_btn.click()
        signin_btn = WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/login"]')))
        assert signin_btn.is_displayed()
