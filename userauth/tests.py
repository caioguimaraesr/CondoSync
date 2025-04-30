import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

class CadastroTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_cadastro_user(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/') 

        time.sleep(1)

        register_button = driver.find_element(By.ID, 'register')
        register_button.click()

        time.sleep(1)

        first_name_field = driver.find_element(By.NAME, 'first_name')
        last_name_field = driver.find_element(By.NAME, 'last_name')
        username_field = driver.find_element(By.NAME, 'username')
        email_field = driver.find_element(By.NAME, 'email')
        password_field = driver.find_element(By.NAME, 'password')
        confirm_password_field = driver.find_element(By.NAME, 'confirm_password')
        apartamento_select = driver.find_element(By.NAME, 'apartamento')

        first_name_field.send_keys('user')
        last_name_field.send_keys('teste')
        username_field.send_keys('userteste')
        email_field.send_keys('userteste@gmail.com')
        password_field.send_keys('User@teste2025')
        confirm_password_field.send_keys('User@teste2025')

        apartamento_select.click()
        apartamento_select.find_element(By.XPATH, '//option[not(@disabled)]').click()

        usuario_checkbox = driver.find_element(By.NAME, 'usuario')
        usuario_checkbox.click()

        submit_button = driver.find_element(By.TAG_NAME, 'button')
        submit_button.click()

        time.sleep(1)

        self.assertIn('/', driver.current_url)

    def test_cadastro_admin(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/') 

        time.sleep(1)

        register_button = driver.find_element(By.ID, 'register')
        register_button.click()

        time.sleep(1)

        first_name_field = driver.find_element(By.NAME, 'first_name')
        last_name_field = driver.find_element(By.NAME, 'last_name')
        username_field = driver.find_element(By.NAME, 'username')
        email_field = driver.find_element(By.NAME, 'email')
        password_field = driver.find_element(By.NAME, 'password')
        confirm_password_field = driver.find_element(By.NAME, 'confirm_password')
        apartamento_select = driver.find_element(By.NAME, 'apartamento')

        first_name_field.send_keys('admin')
        last_name_field.send_keys('teste')
        username_field.send_keys('adminteste')
        email_field.send_keys('adminteste@gmail.com')
        password_field.send_keys('Admin@teste2025')
        confirm_password_field.send_keys('Admin@teste2025')

        apartamento_select.click()
        apartamento_select.find_element(By.XPATH, '//option[not(@disabled)]').click()

        usuario_checkbox = driver.find_element(By.NAME, 'admin')
        usuario_checkbox.click()

        time.sleep(1) 
        admin_password_field = driver.find_element(By.NAME, 'admin_password')
        admin_password_field.send_keys('senha')

        submit_button = driver.find_element(By.TAG_NAME, 'button')
        submit_button.click()

        time.sleep(1)

        self.assertIn('/', driver.current_url)

    def tearDown(self):
        self.driver.quit()

class LoginTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_login_user(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/')

        time.sleep(1)

        login_div = driver.find_element(By.CLASS_NAME, 'sign-in')

        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')

        username_field.send_keys('userteste') 
        password_field.send_keys('User@teste2025')

        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

        time.sleep(1)

        self.assertIn('condosync/home/', driver.current_url)

    def test_login_admin(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/')

        time.sleep(1)

        login_div = driver.find_element(By.CLASS_NAME, 'sign-in')

        username_field = login_div.find_element(By.NAME, 'username')
        password_field = login_div.find_element(By.NAME, 'password')

        username_field.send_keys('adminteste') 
        password_field.send_keys('Admin@teste2025')

        login_button = login_div.find_element(By.TAG_NAME, 'button')
        login_button.click()

        time.sleep(1)

        self.assertIn('condosync/home/', driver.current_url)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()