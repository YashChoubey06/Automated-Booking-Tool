# Selenium Gym Class Booking Bot

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-4.x-green?style=for-the-badge&logo=selenium)

This project is a Python-based automation bot that scrapes a dynamic gym schedule and automatically books classes. It's designed to be robust, handling persistent logins, various button states, and network timeouts.

The primary goal of this bot is to demonstrate advanced Selenium techniques for handling a real-world, dynamic web application.

---

## 🚀 Key Features

This bot was built to overcome common challenges in web automation:

* **Persistent Login:** The bot uses a persistent Chrome profile (`--user-data-dir`). This saves your login session, so you only need to log in manually the very first time. On all future runs, the bot "remembers" who you are.
* **Dynamic Content Handling:** The script doesn't rely on static IDs. It scans the page for dynamically generated "class cards" and "day groups," filtering them by day and time to find the correct classes.
* **Smart Booking Logic:** It intelligently handles different button states. The bot checks if a class button says "Book Class," "Join Waitlist," "Booked," or "Waitlisted" and takes the appropriate action (or skips if already done).
* **Robust Retry Mechanism:** A higher-order function (`retry()`) acts as a wrapper for critical actions like logging in and booking. If a network error or `TimeoutException` occurs, it automatically re-attempts the action up to 7 times before failing.
* **Automated Booking Verification (QA):** After attempting to book, the bot performs a quality assurance check. It navigates to the "My Bookings" page, scrapes the list of confirmed classes, and verifies that the number of expected bookings matches what's actually on the page.

---

## 🛠️ Tech Stack

* **Core:** Python
* **Browser Automation:** Selenium
    * `webdriver.Chrome`: To control the Chrome browser.
    * `WebDriverWait` & `expected_conditions`: For explicitly waiting for elements to load, preventing flakiness.
    * `By` (ID, CSS_SELECTOR, XPATH): For locating elements.
* **Error Handling:** Explicitly catches `TimeoutException` and `NoSuchElementException` to manage the retry logic.
* **Standard Libraries:** `os` (for managing file paths for the user profile) and `time` (for delays).

---

## ⚙️ How It Works

1.  **Initialize:** The script launches a new Chrome session, telling it to use a local `chrome_profile` directory to store session data.
2.  **Login:** It navigates to the gym's URL and calls the `login()` function (wrapped in a `retry` block). On first run, you'll log in. On subsequent runs, this step will be skipped as the session is already active.
3.  **Find Classes:** The `bookClass()` function is called with the desired days (e.g., "Tue", "Thu") and time slots.
4.  **Scrape & Filter:** The bot finds all `div[id^='class-card-']` elements on the page. It iterates through each one, checking its parent "day group" and its "class time" to see if it matches the user's criteria.
5.  **Act:** For each matching class, it checks the button text.
    * `"Book Class"` -> Clicks "Book".
    * `"Join Waitlist"` -> Clicks "Join Waitlist".
    * `"Booked"` / `"Waitlisted"` -> Skips and logs as "Already Booked."
6.  **Verify:** After the booking loop, the `verifyBookings()` function is called. It clicks the "My Bookings" link, scrapes the resulting page, and counts how many of the classes it just tried to book are present.
7.  **Report:** The script prints a detailed summary of all actions taken and the final verification status (Success or Mismatch) to the console.
