import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

WAIT_TIME = 10

class LoginLogoutTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(WAIT_TIME)
        self.base_url = "http://127.0.0.1:8000/"

    def tearDown(self):
        self.driver.quit()

    def _navigate_to_login(self):
        self.driver.get(self.base_url)
        login_link = self.driver.find_element(By.CSS_SELECTOR, 'a.btn.btn-primary[href="/login/"]')
        login_link.click()

    def _fill_credentials(self, email, password):
        email_field = self.driver.find_element(By.ID, "id_email")
        email_field.clear()
        email_field.send_keys(email)
        password_field = self.driver.find_element(By.ID, "id_password")
        password_field.clear()
        password_field.send_keys(password)

    def _click_login_submit(self):
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"].btn.btn-primary')
        submit_button.click()

    def _get_second_to_last_link_element(self):
        links_div = self.driver.find_element(By.CSS_SELECTOR, "div.links")
        children = links_div.find_elements(By.XPATH, "./*")
        return children[-2]
    
    def test_login_logout_and_invalid_login(self):
        # navigate and log in with valid credentials
        self._navigate_to_login()
        self._fill_credentials("aaa@gmail.com", "aaa_password")
        time.sleep(WAIT_TIME)

        self._click_login_submit()
        time.sleep(WAIT_TIME)

        # verify successful login
        indicator = self._get_second_to_last_link_element()
        self.assertEqual(indicator.tag_name, "span")
        self.assertIn("user-info", indicator.get_attribute("class"))
        print("Login with valid credentials - OK")

        # click logout
        logout_link = self.driver.find_element(By.CSS_SELECTOR, 'nav a[href="/logout/"]')
        logout_link.click()
        time.sleep(WAIT_TIME)

        # verify successful logout
        indicator = self._get_second_to_last_link_element()
        self.assertEqual(indicator.tag_name, "a")
        self.assertEqual(indicator.get_attribute("href"), self.base_url + "login/")
        self.assertEqual(indicator.text, "Login")
        print("Logout - OK")

        # navigate to login and enter invalid credentials
        self._navigate_to_login()
        time.sleep(WAIT_TIME)
        self._fill_credentials("aaa@gmail.com", "password")
        self._click_login_submit()
        time.sleep(WAIT_TIME)

        # verify error message is displayed
        error_message = self.driver.find_element(By.XPATH, '//p[text()="Invalid email or password."]')
        self.assertTrue(error_message.is_displayed())
        print("Error for invalid credentials - OK")
        
        # verify user is still not logged in ---
        indicator = self._get_second_to_last_link_element()
        self.assertEqual(indicator.tag_name, "a")
        self.assertEqual(indicator.get_attribute("href"), self.base_url + "login/")
        self.assertEqual(indicator.text, "Login")
        print("No login happens with invalid credentials - OK")

if __name__ == "__main__":
    unittest.main()
