from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os

ACCOUNT_EMAIL = "test@test.com"
ACCOUNT_PASSWORD = "password"
GYM_URL = "https://appbrewery.github.io/gym/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
driver = webdriver.Chrome(options=chrome_options)

wait = WebDriverWait(driver, 2)

driver.get(GYM_URL)

login_button = driver.find_element(By.ID, "login-button")
login_button.click()

email = driver.find_element(By.ID, "email-input")
email.send_keys(ACCOUNT_EMAIL)
password = driver.find_element(By.ID, "password-input")
password.send_keys(ACCOUNT_PASSWORD)

submit_button = driver.find_element(By.ID, "submit-button")
submit_button.click()

wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))

