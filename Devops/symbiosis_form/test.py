import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

def run_tests():
    # Setup Chrome options
    chrome_options = Options()
    # Removed headless mode so the browser window is visible
    # chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Construct absolute path to the local html file
        file_path = "file:///" + os.path.abspath("index.html").replace('\\', '/')
        print(f"Opening {file_path}")
        driver.get(file_path)
        time.sleep(2) # Added delay to see the initial page
        
        # Helper to check if element is displayed
        def is_displayed(element_id):
            return driver.find_element(By.ID, element_id).is_displayed()
        
        print("\n--- Test 1: Empty Form Submission ---")
        driver.find_element(By.ID, "submitBtn").click()
        time.sleep(2) # wait for JS validation and see the errors
        
        assert is_displayed("emailError"), "Email error should be visible"
        assert is_displayed("passwordError"), "Password error should be visible"
        assert is_displayed("confirmPasswordError"), "Confirm Password error should be visible"
        assert is_displayed("genderError"), "Gender error should be visible"
        assert is_displayed("courseError"), "Course error should be visible"
        print("Test 1 passes: Correct validation messages for empty form.")

        print("\n--- Test 2: Invalid Email and Password Mismatch ---")
        driver.find_element(By.ID, "email").send_keys("invalidemail")
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys("12345") # < 6 chars
        time.sleep(1)
        driver.find_element(By.ID, "confirm_password").send_keys("123456") # Mismatch
        time.sleep(1)
        driver.find_element(By.ID, "submitBtn").click()
        time.sleep(2)
        
        assert is_displayed("emailError"), "Email error should still be visible"
        assert is_displayed("passwordError"), "Password error should be visible (<6 chars)"
        assert is_displayed("confirmPasswordError"), "Confirm Password error should be visible (mismatch)"
        print("Test 2 passes: Correct validation for improper email & passwords.")

        print("\n--- Test 3: Multiple Checkboxes Selected for Gender ---")
        driver.find_element(By.ID, "email").clear()
        time.sleep(0.5)
        driver.find_element(By.ID, "email").send_keys("test@example.com")
        time.sleep(1)
        
        driver.find_element(By.ID, "password").clear()
        time.sleep(0.5)
        driver.find_element(By.ID, "password").send_keys("securepassword")
        time.sleep(1)
        
        driver.find_element(By.ID, "confirm_password").clear()
        time.sleep(0.5)
        driver.find_element(By.ID, "confirm_password").send_keys("securepassword")
        time.sleep(1)

        # Select two checkboxes
        driver.find_element(By.ID, "gender_male").click()
        time.sleep(0.5)
        driver.find_element(By.ID, "gender_female").click()
        time.sleep(1)
        
        # Select course
        Select(driver.find_element(By.ID, "course")).select_by_value("B.Tech")
        time.sleep(1)
        
        driver.find_element(By.ID, "submitBtn").click()
        time.sleep(2)
        
        assert is_displayed("genderError"), "Gender error should be visible because >1 checkbox is selected"
        assert not is_displayed("emailError"), "Email error should not be visible"
        assert not is_displayed("passwordError"), "Password error should not be visible"
        assert not is_displayed("courseError"), "Course error should not be visible"
        print("Test 3 passes: Correct validation for multiple checkboxes selected.")

        print("\n--- Test 4: Successful Submission ---")
        # Uncheck female so only one is checked
        driver.find_element(By.ID, "gender_female").click()
        time.sleep(1)
        
        driver.find_element(By.ID, "submitBtn").click()
        time.sleep(3) # Leave successful view for a moment longer
        
        assert is_displayed("success"), "Success message should be visible"
        print("Test 4 passes: Form submitted successfully.")

    finally:
        time.sleep(2) # Final delay before closing
        driver.quit()

if __name__ == "__main__":
    run_tests()
