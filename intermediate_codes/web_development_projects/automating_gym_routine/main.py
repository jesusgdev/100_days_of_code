from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from dotenv import load_dotenv
import calendar
import time
import os

DAYS_OF_THE_WEEK = list(calendar.day_name)

load_dotenv()
ACCOUNT_EMAIL = os.environ["ACCOUNT_EMAIL"]
ACCOUNT_PASSWORD = os.environ["ACCOUNT_PASSWORD"]

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(name="detach", value=True)

# User profile
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# Create a driver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the webpage
URL = "https://appbrewery.github.io/gym/"
driver.get(url=URL)

wait = WebDriverWait(driver, timeout=2)


def login():
    login_button = driver.find_element(by=By.ID, value="login-button")
    login_button.click()

    time.sleep(0.5)

    email = driver.find_element(by=By.ID, value="email-input")
    email.clear()
    email.send_keys(ACCOUNT_EMAIL)

    password = driver.find_element(by=By.ID, value="password-input")
    password.clear()
    password.send_keys(ACCOUNT_PASSWORD)

    submit_button = driver.find_element(by=By.ID, value="submit-button")
    submit_button.click()

    wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))


def retry(func, retries=7, description=None):
    for n in range(retries):
        print(f"Trying {description}. Attempt: {n + 1}")
        try:
            return func()
        except TimeoutException:
            if n == retries - 1:
                raise
            time.sleep(1)


def click_until_success(button, max_attempts=5):
    """
    Simple function: Click button until the click works (50% network fail).

    Args:
        button: The button element to click
        max_attempts: Maximum number of click attempts

    Returns:
        bool: True if click succeeded, False otherwise
    """
    initial_text = button.text

    for attempt in range(1, max_attempts + 1):
        try:
            print(f"  → Attempt {attempt}: Clicking '{initial_text}'...")
            button.click()

            # Wait a moment for the change to happen
            time.sleep(2)

            # Check if button text changed (means click worked)
            if button.text != initial_text:
                print(f"  ✓ Success! Changed to '{button.text}'")
                return True
            else:
                print(f"  ✗ No change, retrying...")

        except Exception as e:
            print(f"  ✗ Error on attempt {attempt}: {e}")
            time.sleep(0.5)

    print(f"  ✗ Failed after {max_attempts} attempts")
    return False


# def click_and_wait_for_h1(link, expected_h1_text, max_attempts=5):
#     """
#     Click link and wait for h1 with specific text to appear.
#     """
#     for attempt in range(1, max_attempts + 1):
#         try:
#             print(f"  → Attempt {attempt}: Navigating...")
#             link.click()
#             time.sleep(0.5)
#
#             h1 = driver.find_element(by=By.TAG_NAME, value="h1")
#             if h1.text == expected_h1_text:
#                 print(f"  ✓ Successfully navigated to {expected_h1_text}")
#                 return True
#             else:
#                 print(f"  ✗ Wrong page (found: {h1.text}), retrying...")
#         except Exception as e:
#             print(f"  ✗ Error: {e}")
#             time.sleep(0.5)
#
#     return False

retry(login, description="login")

print("\n✓ Successfully logged\n")


def booking_class():
    class_schedule_days = driver.find_elements(by=By.CLASS_NAME, value="Schedule_dayGroup__y79__")

    booked_count = 0
    waitlist_count = 0
    already_booked_waitlisted = 0
    class_time = ""
    processed_class = 0
    verification_count = 0
    class_list = []
    my_bookings = []

    for each_day in class_schedule_days:

        class_date_tag = each_day.find_element(by=By.TAG_NAME, value="h2").text

        if "Tomorrow" in class_date_tag or "Today" in class_date_tag:
            start = class_date_tag.index("(") + 1
            end = class_date_tag.index(")")
            class_date_tag = class_date_tag[start:end]

        if "Tue" in class_date_tag or "Thu" in class_date_tag:
            class_day = class_date_tag.split()[0].replace(",", "")
            class_date = class_date_tag
            class_activities = each_day.find_elements(by=By.CLASS_NAME, value="ClassCard_card__KpCx5")

            for activity in class_activities:

                class_time = activity.find_element(by=By.TAG_NAME, value="p").text.replace("Time: ", "")
                class_name = activity.find_element(by=By.TAG_NAME, value="h3").text

                if class_time == "6:00 PM":
                    join_class_button = activity.find_element(by=By.TAG_NAME, value="button")
                    class_hour = class_time
                    status = join_class_button.text

                    # Only click if NOT already booked/waitlisted
                    if status not in ["Booked", "Waitlisted"]:
                        print(f"Booking: {class_name} on {class_date}")
                        click_until_success(join_class_button, max_attempts=5)
                        # Update status after clicking
                        status = join_class_button.text

                    # Report the result
                    if status == "Waitlisted":
                        print(f"✓ Already on waitlist: {class_name} on {class_date}")
                        already_booked_waitlisted += 1
                    elif status == "Booked":
                        print(f"✓ Already booked: {class_name} on {class_date}")
                        already_booked_waitlisted += 1
                    elif status == "Join Waitlist":
                        print(f"✓ Joined waitlist for: {class_name} on {class_date}")
                        waitlist_count += 1
                    else:
                        print(f"✓ Successfully Booked: {class_name} on {class_date}")
                        booked_count += 1

                    class_list.append({
                        "class": class_name,
                        "day": class_day,
                        "status": status,
                        "date": class_date,
                    })

                    processed_class += 1

    # Convert day abbreviations to full names
    for day in DAYS_OF_THE_WEEK:
        for class_info in class_list:
            if class_info["day"] in day:
                class_info["day"] = day

    # Print summary
    if len(class_list) > 1:
        print(
            f"\n--- Total processed {class_list[0]['day']}/{class_list[1]['day']} {class_hour} classes: {processed_class} ---\n")
    else:
        print(f"\n--- Total processed {class_list[0]['day']} {class_hour} classes: {processed_class} ---\n")

    # Go to My Bookings page
    my_booking_link = driver.find_element(by=By.ID, value="my-bookings-link")
    my_booking_link.click()

    # Wait for bookings page to load
    time.sleep(1)

    # Verify bookings
    confirmed_booked_classes = driver.find_elements(by=By.CLASS_NAME, value="MyBookings_bookingCard__VRdrR")

    for tag in confirmed_booked_classes:
        class_name = tag.find_element(by=By.TAG_NAME, value="h3").text
        reserve_type = tag.find_element(by=By.TAG_NAME, value="button").text.split()[1]
        verification_count += 1

        my_bookings.append({
            "class": class_name,
            "reserve_type": reserve_type,
        })

    print("--- VERIFYING ON MY BOOKINGS PAGE ---")
    for reserve in my_bookings:
        print(f"✓ Verified: {reserve['class']}")

    print("\n--- VERIFICATION RESULT ---")
    print(f"Expected: {processed_class} bookings")
    print(f"Found: {verification_count} bookings")

    if processed_class == verification_count:
        print("✅ SUCCESS: All bookings verified!")
    else:
        print(f"❌ MISMATCH: Difference of {abs(processed_class - verification_count)} bookings")


retry(booking_class, description="Booking")