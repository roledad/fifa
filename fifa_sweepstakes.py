"""
FIFA World Cup 26 Perks Sweepstakes Automation
Automates entering daily sweepstakes on fwc26perks.com
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from datetime import datetime
from typing import Dict, Optional


class FIFASweepstakesBot:
    """Automates FIFA World Cup 26 Perks sweepstakes entry"""

    def __init__(self,
                 headless: bool = True,
                 wait_timeout: int = 10):
        """
        Initialize the bot

        Args:
            headless: Run browser in headless mode (default: True, browser hidden)
            wait_timeout: Timeout for waiting for elements (seconds)
        """
        self.url = "https://www.fwc26perks.com/"
        self.wait_timeout = wait_timeout
        self.driver = None
        self._in_iframe = False  # Track if we're in an iframe context
        self.setup_driver(headless)

    def setup_driver(self, headless: bool = True):
        """Setup Selenium WebDriver"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception(f"Failed to setup WebDriver: {e}. Make sure ChromeDriver is installed.")

    def wait_for_element(self, by: By, value: str, timeout: Optional[int] = None):
        """Wait for an element to be present"""
        timeout = timeout or self.wait_timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    def wait_for_clickable(self, by: By, value: str, timeout: Optional[int] = None):
        """Wait for an element to be clickable"""
        timeout = timeout or self.wait_timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, value)))

    def wait_for_presence(self, by: By, value: str, timeout: Optional[int] = None):
        """Wait for an element to be present (not necessarily clickable)"""
        timeout = timeout or self.wait_timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    def navigate_to_site(self):
        """Navigate to the sweepstakes website"""
        print(f"Navigating to {self.url}...")
        self.driver.get(self.url)
        time.sleep(3)  # Wait for page to load

    def select_sweepstakes(self, sweepstakes_number: int = 3):
        """Click the 'Select' button for a specific sweepstakes (default: sweepstakes 3)"""
        print(f"Selecting sweepstakes {sweepstakes_number}...")

        # Find all select buttons - they have the class "select-button"
        try:
            select_buttons = self.driver.find_elements(By.CSS_SELECTOR, "a.select-button.w-button")

            if not select_buttons:
                # Try alternative selector
                select_buttons = self.driver.find_elements(By.XPATH, "//a[contains(@class, 'select-button')]")

            print(f"Found {len(select_buttons)} select button(s)")

            # Check if the requested sweepstakes number is valid
            if sweepstakes_number < 1 or sweepstakes_number > len(select_buttons):
                print(f"  ✗ Invalid sweepstakes number {sweepstakes_number}. Available: 1-{len(select_buttons)}")
                return 0

            # Select the specific sweepstakes (convert to 0-based index)
            button_index = sweepstakes_number - 1
            button = select_buttons[button_index]

            try:
                # Scroll to button
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                time.sleep(0.5)

                # Click the button
                button.click()
                print(f"  ✓ Selected sweepstakes {sweepstakes_number}")
                time.sleep(1)  # Wait for selection to process
                return 1
            except Exception as e:
                print(f"  ✗ Failed to select sweepstakes {sweepstakes_number}: {e}")
                return 0

        except Exception as e:
            print(f"Error finding select buttons: {e}")
            return 0

    def find_and_switch_to_iframe(self):
        """Find iframe containing the form and switch to it"""
        # Find all iframes
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")

        # Try to switch to each iframe and check if it contains our form fields
        for iframe in iframes:
            try:
                self.driver.switch_to.frame(iframe)
                time.sleep(1)  # Wait for iframe content to load

                # Check if we can find any of our target fields
                target_fields = ['first', 'last', 'email', 'confirmEmail', 'zip', 'aaNumber']
                found_count = 0

                for field_id in target_fields:
                    try:
                        self.driver.find_element(By.ID, field_id)
                        found_count += 1
                    except:
                        pass

                if found_count > 0:
                    print(f"✓ Switched to iframe (found {found_count} form fields)")
                    return True
                else:
                    # Switch back to default content
                    self.driver.switch_to.default_content()

            except Exception as e:
                # Make sure we're back to default content
                try:
                    self.driver.switch_to.default_content()
                except:
                    pass

        print("✓ Form is on main page (no iframe)")
        return False

    def fill_form(self, form_data: Dict[str, str]):
        """
        Fill in the form with provided data

        Args:
            form_data: Dictionary with form field IDs and values
        """
        print("Filling form...")

        # First, try to find and switch to iframe if form is inside one
        switched_to_iframe = self.find_and_switch_to_iframe()
        self._in_iframe = switched_to_iframe

        # Wait for dynamic content to load
        time.sleep(2)

        field_mapping = {
            'first': 'first',
            'last': 'last',
            'email': 'email',
            'confirmEmail': 'confirmEmail',
            'zip': 'zip',
            'aaNumber': 'aaNumber'
        }

        for field_key, field_id in field_mapping.items():
            if field_key in form_data:
                element = None

                # Try to find the element by ID first (most common)
                try:
                    element = self.wait_for_clickable(By.ID, field_id, timeout=3)
                except (TimeoutException, NoSuchElementException):
                    # Try by name as fallback
                    try:
                        element = self.wait_for_clickable(By.NAME, field_id, timeout=2)
                    except:
                        pass

                if element:
                    try:
                        # Scroll element into view
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                        time.sleep(0.3)

                        # Clear and fill
                        element.clear()
                        time.sleep(0.2)
                        element.send_keys(form_data[field_key])
                        print(f"  ✓ Filled {field_key}: {form_data[field_key]}")
                        time.sleep(0.3)
                    except Exception as e:
                        print(f"  ✗ Error filling {field_id}: {e}")
                else:
                    print(f"  ✗ Could not find field '{field_id}'")

    def check_all_checkboxes(self):
        """Check all checkboxes on the form"""
        print("Checking all checkboxes...")

        try:
            # Find all checkboxes that are not already checked
            checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")

            checked_count = 0
            for i, checkbox in enumerate(checkboxes, 1):
                try:
                    # Scroll to checkbox
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                    time.sleep(0.3)

                    # Check if not already checked
                    if not checkbox.is_selected():
                        checkbox.click()
                        checked_count += 1
                        print(f"  ✓ Checked checkbox {i}")
                    else:
                        print(f"  - Checkbox {i} already checked")

                    time.sleep(0.3)
                except Exception as e:
                    print(f"  ✗ Failed to check checkbox {i}: {e}")
                    continue

            print(f"Checked {checked_count} checkbox(es)")
            return checked_count
        except Exception as e:
            print(f"Error finding checkboxes: {e}")
            return 0

    def find_and_click_submit(self):
        """Find and click the submit button"""
        print("Looking for submit button...")

        # Try multiple possible selectors for submit button
        submit_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button.submit",
            ".submit-button",
            "//button[contains(text(), 'Submit')]",
            "//button[contains(text(), 'Enter')]",
            "//input[contains(@value, 'Submit')]",
            "//input[contains(@value, 'Enter')]"
        ]

        for selector in submit_selectors:
            try:
                if selector.startswith("//"):
                    # XPath selector
                    button = self.wait_for_clickable(By.XPATH, selector)
                else:
                    # CSS selector
                    button = self.wait_for_clickable(By.CSS_SELECTOR, selector)

                # Scroll to button
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                time.sleep(1)

                # Click submit
                button.click()
                print(f"  ✓ Clicked submit button (found with: {selector})")
                time.sleep(3)  # Wait for submission to process
                return True
            except (TimeoutException, NoSuchElementException):
                continue
            except Exception as e:
                print(f"  Error with selector {selector}: {e}")
                continue

        print("  ✗ Could not find submit button")
        return False

    def submit_form(self, form_data: Dict[str, str]):
        """
        Complete the entire process:
        1. Navigate to site
        2. Select all sweepstakes
        3. Fill form
        4. Check all checkboxes
        5. Submit

        Args:
            form_data: Dictionary with form field values
        """
        try:
            # Navigate to site
            self.navigate_to_site()

            # Scroll down to find form elements
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(2)

            # Select sweepstakes 3
            self.select_sweepstakes(3)
            time.sleep(2)

            # Scroll to form area
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Fill form
            self.fill_form(form_data)
            time.sleep(1)

            # Check all checkboxes
            self.check_all_checkboxes()
            time.sleep(1)

            # Scroll down more in case submit button is below
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            # Submit
            success = self.find_and_click_submit()

            if success:
                print("\n✓ Form submitted successfully!")
                print("Waiting 5 seconds to see confirmation...")
                time.sleep(5)

                # Check for success message or error
                try:
                    page_text = self.driver.page_source.lower()
                    if 'thank' in page_text or 'success' in page_text or 'submitted' in page_text:
                        print("✓ Submission appears successful!")
                        # Save screenshot after confirmation
                        self.save_submission_screenshot()
                    elif 'error' in page_text or 'invalid' in page_text:
                        print("⚠ Warning: Page may contain errors")
                        self.save_submission_screenshot()
                except:
                    pass
            else:
                print("\n✗ Could not find submit button. Please check manually.")

        except Exception as e:
            print(f"\n✗ Error during submission: {e}")
            import traceback
            traceback.print_exc()

    def save_submission_screenshot(self):
        """Save a screenshot of the webpage after submission confirmation"""
        try:
            # Get current date in YYYY-MM-DD format
            date_str = datetime.now().strftime('%Y-%m-%d')
            screenshot_filename = f"submission_{date_str}.png"

            # Save screenshot
            self.driver.save_screenshot(screenshot_filename)
            print(f"  ✓ Screenshot saved: {screenshot_filename}")
            return screenshot_filename
        except Exception as e:
            print(f"  ✗ Error saving screenshot: {e}")
            return None

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


def main():
    """Main execution function"""
    # Import config or use defaults
    try:
        from config import FORM_DATA, HEADLESS, WAIT_TIMEOUT
        form_data = FORM_DATA
        headless = HEADLESS
        wait_timeout = WAIT_TIMEOUT
    except ImportError:
        # Fallback to defaults if config.py doesn't exist
        print("No config.py found, please create one and add your personal information. Exiting...")
        exit(1)

    print("=" * 60)
    print("FIFA World Cup 26 Perks Sweepstakes Bot")
    print("=" * 60)
    if form_data:
        print(f"Entering sweepstakes for: {form_data['first']} {form_data['last']}")
        print(f"Email: {form_data['email']}")
    print()

    with FIFASweepstakesBot(headless=headless, wait_timeout=wait_timeout) as bot:
        bot.submit_form(form_data)

    if headless == False:  # If not headless, wait for 5 seconds to see the browser close
        print("\nBrowser will close in 5 seconds...")
        time.sleep(5)
    print("Done!")

if __name__ == '__main__':
    main()
