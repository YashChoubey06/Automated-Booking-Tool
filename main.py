from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os
import time

def retry(func, retries=7, description=None):
    for i in range(retries):
        print(f"Trying {description}. Attempt: {i + 1}")
        try:
            return func()
        except TimeoutException:
            if i == retries - 1:
                raise
            time.sleep(1)


def bookClass(*days, **kwargs):
    import time

    time_slots = kwargs.get("time_slots", ["6:00 PM"])

    booked_count = 0
    waitlist_count = 0
    already_count = 0
    total_classes = 0

    details = []

    class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

    for card in class_cards:
        day_group = card.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
        day_title = day_group.find_element(By.TAG_NAME, "h2").text

        if any(day in day_title for day in days):
            time_text = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text

            if any(slot in time_text for slot in time_slots):
                total_classes += 1
                class_name = card.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']").text
                button = card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")
                button_text = button.text

                if button_text == "Booked":
                    already_count += 1
                    details.append(f"  • [Already Booked] {class_name} on {day_title}")

                elif button_text == "Waitlisted":
                    already_count += 1
                    details.append(f"  • [Already Waitlisted] {class_name} on {day_title}")

                elif button_text == "Join Waitlist":
                    button.click()
                    waitlist_count += 1
                    details.append(f"  • [New Waitlist] {class_name} on {day_title}")
                    time.sleep(0.5)

                elif button_text == "Book Class":
                    button.click()
                    booked_count += 1
                    details.append(f"  • [New Booking] {class_name} on {day_title}")
                    time.sleep(0.5)

                else:
                    details.append(f"  • [Error] {class_name} on {day_title} — Unexpected button state.")

    # print("\n--- BOOKING SUMMARY ---")
    # print(f"New bookings: {booked_count}")
    # print(f"New waitlist entries: {waitlist_count}")
    # print(f"Already booked/waitlisted: {already_count}")
    # print(f"Total {' & '.join(days)} {'/'.join(time_slots)} classes: {total_classes}")

    print("\n--- DETAILED CLASS LIST ---")
    if details:
        for line in details:
            print(line
                  )
    else:
        print("No matching classes found.\n")

    retry(
        lambda: verifyBookings(total_classes, *days, time_slots=time_slots),
        description="verifying bookings"
    )

    print("\n✨ Booking process completed successfully!\n")


def verifyBookings(total, *days, **kwargs):
    time_slots = kwargs.get("time_slots", [])

    print(f"\n--- Total {' / '.join(days)} {', '.join(time_slots)} classes: {total} ---")
    print("\n--- VERIFYING ON MY BOOKINGS PAGE ---")
    verified_count = 0

    my_bookings = driver.find_element(By.ID, "my-bookings-link")
    my_bookings.click()

    all_cards = driver.find_elements(By.CSS_SELECTOR, "div[id*='card-']")
    detailed_verified = []

    for card in all_cards:
        try:
            when_paragraph = card.find_element(By.XPATH, ".//p[strong[text()='When:']]")
            when_text = when_paragraph.text

            if any(day in when_text for day in days) and any(slot in when_text for slot in time_slots):
                class_name = card.find_element(By.TAG_NAME, "h3").text
                print(f"  ✓ Verified: {class_name} ({when_text})")
                detailed_verified.append(f"  • [Verified] {class_name} ({when_text})")
                verified_count += 1
        except NoSuchElementException:
            pass

    print(f"\n--- VERIFICATION RESULT ---")
    print(f"Expected: {total} bookings")
    print(f"Found: {verified_count} bookings")

    if total == verified_count:
        print("✅ SUCCESS: All bookings verified!")
    else:
        print(f"❌ MISMATCH: Missing {total - verified_count} bookings")

    print("\n--- DETAILED VERIFIED LIST ---")
    if detailed_verified:
        for line in detailed_verified:
            print(line)
    else:
        print("No matching bookings found.")


def login():

    login_btn = wait.until(ec.element_to_be_clickable((By.ID, "login-button")))
    login_btn.click()

    email_input = wait.until(ec.presence_of_element_located((By.ID, "email-input")))
    email_input.clear()
    email_input.send_keys(ACCOUNT_EMAIL)

    password_input = driver.find_element(By.ID, "password-input")
    password_input.clear()
    password_input.send_keys(ACCOUNT_PASSWORD)

    submit_btn = driver.find_element(By.ID, "submit-button")
    submit_btn.click()

    wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))


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

retry(login, description="login")
retry(
    lambda: bookClass("Tue","Thu"),
    description="booking"
)
