import os
import sys
import time
import calendar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Target days and time for class booking
TARGET_DAYS = ["Tue", "Thu"]  # Days to book classes
TARGET_TIME = "6:00 PM"  # Preferred class time
DAYS_OF_THE_WEEK = list(calendar.day_name)

# Network retry settings
MAX_LOGIN_RETRIES = 7  # Maximum login attempts
MAX_BOOKING_RETRIES = 7  # Maximum booking process attempts
MAX_CLICK_RETRIES = 5  # Maximum retries for individual button clicks

# Load credentials from .env file
load_dotenv()
ACCOUNT_EMAIL = os.getenv("ACCOUNT_EMAIL")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")

if not ACCOUNT_EMAIL or not ACCOUNT_PASSWORD:
    raise ValueError("Missing credentials in .env file. Please add ACCOUNT_EMAIL and ACCOUNT_PASSWORD")

# ==============================================================================
# SETUP CHROME DRIVER
# ==============================================================================

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(name="detach", value=True)

# Use persistent Chrome profile to save login sessions
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# Initialize Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to gym booking website
GYM_URL = "https://appbrewery.github.io/gym/"
driver.get(GYM_URL)

print(f"Navigated to: {GYM_URL}\n")


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def retry_with_attempts(func, retries, description):
    """
    Retry a function multiple times if it fails.

    Args:
        func: Function to execute
        retries: Maximum number of retry attempts
        description: Description for logging

    Returns:
        Result of the function if successful
    """
    for attempt in range(1, retries + 1):
        print(f"Trying {description}. Attempt: {attempt}/{retries}")
        try:
            return func()
        except TimeoutException as e:
            if attempt == retries:
                # Final attempt failed - display friendly error and exit
                print("\n" + "=" * 70)
                print(f"❌ ERROR: {description} Failed After {retries} Attempts")
                print("=" * 70)
                print("Reason: Network timeout - the page did not load in time")
                print("\nPossible causes:")
                print("  • Internet connection is slow or unstable")
                print("  • Gym website is down or not responding")
                print("  • Firewall or antivirus blocking connection")
                print("\nPlease check your connection and try again.")
                print("=" * 70 + "\n")
                driver.quit()
                sys.exit(1)

            print(f"✗ Attempt {attempt} failed, retrying...\n")
            time.sleep(1)


def click_until_text_changes(button, max_attempts=5):
    """
    Click button repeatedly until text changes (handles 50% network failure).

    Args:
        button: Selenium WebElement to click
        max_attempts: Maximum number of click attempts

    Returns:
        bool: True if button text changed, False otherwise
    """
    initial_text = button.text

    for attempt in range(1, max_attempts + 1):
        try:
            print(f"  → Attempt {attempt}/{max_attempts}: Clicking '{initial_text}'...")
            button.click()

            # Wait for server response
            time.sleep(2)

            # Verify button text changed (indicates successful click)
            current_text = button.text
            if current_text != initial_text:
                print(f"  ✓ Success! Button changed to '{current_text}'")
                return True
            else:
                print(f"  ✗ No change detected, retrying...")

        except Exception as e:
            print(f"  ✗ Error on attempt {attempt}: {e}")
            time.sleep(0.5)

    print(f"  ✗ Failed after {max_attempts} attempts")
    return False


# ==============================================================================
# STEP 1: Login to gym account
# ==============================================================================

def login():
    """
    Authenticate user with email and password.
    Waits for schedule page to load after successful login.
    """
    # Click login button
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()

    time.sleep(0.5)

    # Enter email
    email_input = driver.find_element(By.ID, "email-input")
    email_input.clear()
    email_input.send_keys(ACCOUNT_EMAIL)

    # Enter password
    password_input = driver.find_element(By.ID, "password-input")
    password_input.clear()
    password_input.send_keys(ACCOUNT_PASSWORD)

    # Submit credentials
    submit_button = driver.find_element(By.ID, "submit-button")
    submit_button.click()

    # Wait for schedule page to load (confirms successful login)
    wait = WebDriverWait(driver, timeout=5)
    wait.until(EC.presence_of_element_located((By.ID, "schedule-page")))


# Execute login with retry mechanism
retry_with_attempts(login, retries=MAX_LOGIN_RETRIES, description="Login")
print("✓ Successfully logged in\n")


# ==============================================================================
# STEP 2: Book classes automatically
# ==============================================================================

def book_classes():
    """
    Main booking function:
    1. Scan schedule for target days and times
    2. Book available classes
    3. Track booking status
    4. Verify bookings on My Bookings page
    """

    # Find all day groups in schedule
    schedule_days = driver.find_elements(By.CLASS_NAME, "Schedule_dayGroup__y79__")

    # Statistics tracking
    booked_count = 0
    waitlist_count = 0
    already_booked_count = 0
    processed_classes = 0

    # Data storage
    class_bookings = []
    verified_bookings = []
    new_button_status = ""

    print("=" * 70)
    print("SCANNING SCHEDULE FOR AVAILABLE CLASSES")
    print("=" * 70 + "\n")

    # ==============================================================================
    # Scan schedule and book classes
    # ==============================================================================

    for day_group in schedule_days:
        # Extract date from heading
        date_heading = day_group.find_element(By.TAG_NAME, "h2").text

        # Parse "Today" or "Tomorrow" dates
        if "Tomorrow" in date_heading or "Today" in date_heading:
            start_idx = date_heading.index("(") + 1
            end_idx = date_heading.index(")")
            date_heading = date_heading[start_idx:end_idx]

        # Check if this is a target day (Tuesday or Thursday)
        if any(day in date_heading for day in TARGET_DAYS):
            day_abbrev = date_heading.split()[0].replace(",", "")
            full_date = date_heading

            # Find all classes on this day
            class_cards = day_group.find_elements(By.CLASS_NAME, "ClassCard_card__KpCx5")

            for card in class_cards:
                # Extract class information
                class_time_raw = card.find_element(By.TAG_NAME, "p").text
                class_time = class_time_raw.replace("Time: ", "")
                class_name = card.find_element(By.TAG_NAME, "h3").text

                # Check if this is the target time
                if class_time == TARGET_TIME:
                    booking_button = card.find_element(By.TAG_NAME, "button")
                    button_status = booking_button.text

                    # Attempt booking if not already booked/waitlisted
                    if button_status not in ["Booked", "Waitlisted"]:
                        print(f"📋 Attempting to book: {class_name} on {full_date}")
                        click_until_text_changes(booking_button, max_attempts=MAX_CLICK_RETRIES)
                        # Update status after click
                        new_button_status = booking_button.text

                    # Log result based on final status
                    if new_button_status:
                        if new_button_status == "Waitlisted":
                            print(f"⏳ Joined waitlist: {class_name} on {full_date}")
                            waitlist_count += 1
                        else:
                            print(f"✓ Successfully booked: {class_name} on {full_date}")
                            booked_count += 1
                    elif button_status == "Waitlisted":
                        print(f"⏳ Already Waitlisted: {class_name} on {full_date}")
                        already_booked_count += 1
                    else:
                        print(f"✓ Already booked: {class_name} on {full_date}")
                        already_booked_count += 1

                    # Store booking information
                    class_bookings.append({
                        "class_name": class_name,
                        "day": day_abbrev,
                        "date": full_date,
                        "status": button_status
                    })

                    processed_classes += 1

    # Convert day abbreviations to full names
    for day_name in DAYS_OF_THE_WEEK:
        for booking in class_bookings:
            if booking["day"] in day_name:
                booking["day"] = day_name

    # ==============================================================================
    # Display booking summary
    # ==============================================================================

    print("\n" + "=" * 70)
    print("BOOKING SUMMARY")
    print("=" * 70)

    if len(class_bookings) > 1:
        days_processed = f"{class_bookings[0]['day']}/{class_bookings[1]['day']}"
    elif len(class_bookings) == 1:
        days_processed = class_bookings[0]['day']
    else:
        days_processed = "None"

    print(f"Days processed: {days_processed}")
    print(f"Target time: {TARGET_TIME}")
    print(f"Total classes processed: {processed_classes}")
    print(f"New bookings: {booked_count}")
    print(f"New Waitlists: {waitlist_count}")
    print(f"Already booked: {already_booked_count}")

    # ==============================================================================
    # Navigate to My Bookings page for verification
    # ==============================================================================

    print("\n" + "=" * 70)
    print("VERIFYING BOOKINGS")
    print("=" * 70 + "\n")

    my_bookings_link = driver.find_element(By.ID, "my-bookings-link")
    my_bookings_link.click()

    # Wait for page to load
    time.sleep(1)

    # Find all booking cards
    booking_cards = driver.find_elements(By.CLASS_NAME, "MyBookings_bookingCard__VRdrR")

    for card in booking_cards:
        class_name = card.find_element(By.TAG_NAME, "h3").text
        reserve_button = card.find_element(By.TAG_NAME, "button")
        reserve_type = reserve_button.text.split()[1]  # "Cancel Booking" or "Leave Waitlist"

        verified_bookings.append({
            "class_name": class_name,
            "reserve_type": reserve_type
        })
        if reserve_type == "Booking":
            print(f"✓ Verified: {class_name} ({reserve_type})")
        else:
            print(f"✓ Verified: {class_name}")

    # ==============================================================================
    # Final verification check
    # ==============================================================================

    print("\n" + "=" * 70)
    print("VERIFICATION RESULT")
    print("=" * 70)

    verification_count = len(verified_bookings)
    print(f"Expected bookings: {processed_classes}")
    print(f"Found in My Bookings: {verification_count}")

    if processed_classes == verification_count:
        print("\n✅ SUCCESS: All bookings verified!")
    else:
        difference = abs(processed_classes - verification_count)
        print(f"\n⚠️  MISMATCH: Difference of {difference} booking(s)")
        print("This may be normal if some classes were full or system errors occurred.")

    print("=" * 70 + "\n")


# Execute booking with retry mechanism
retry_with_attempts(book_classes, retries=MAX_BOOKING_RETRIES, description="Booking")

print("=" * 70)
print("BOOKING PROCESS COMPLETED")
print("=" * 70)

# Keep browser open for user inspection
input("\nPress Enter to close the browser...")
driver.quit()