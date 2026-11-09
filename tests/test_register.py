import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = os.environ.get('TEST_BASE_URL', 'http://127.0.0.1:5000')

@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1280,900')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield browser
    browser.quit()

def get_alert_text(driver):
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = Alert(driver)
    message = alert.text
    alert.accept()
    return message

def test_empty_name(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, 'password').send_keys('testpassword')
    driver.find_element(By.ID, 'submit').click()
    assert get_alert_text(driver) == 'Username cannot be empty'

def test_empty_password(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, 'name').send_keys('student')
    driver.find_element(By.ID, 'submit').click()
    assert get_alert_text(driver) == 'Password cannot be empty'

def test_successful_registration(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, 'name').send_keys('Student')
    driver.find_element(By.ID, 'email').send_keys('student@example.com')
    driver.find_element(By.ID, 'password').send_keys('secret123')
    driver.find_element(By.ID, 'submit').click()
    assert 'Welcome Student' in driver.page_source
