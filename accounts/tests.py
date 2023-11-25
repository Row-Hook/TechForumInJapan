from django.test import LiveServerTestCase
from django.urls import reverse_lazy
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

class TestLogin(LiveServerTestCase):
    selenium=None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Add any other options you need
        cls.selenium = WebDriver(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        #ログインページを開く
        self.selenium.get(self.live_server_url + str(reverse_lazy('account_login')))

        #ログイン
        username_input = self.selenium.find_element(By.NAME,"login")
        username_input.send_keys('hookhamrowan@gmail.com')
        password_input=self.selenium.find_element(By.NAME,'password')
        password_input.send_keys('Iamcool1!')
        self.selenium.find_element(By.CLASS_NAME,'btn').click()

        #ページタイトルの検証
        self.assertEquals('Log In | TechHub', self.selenium.title)