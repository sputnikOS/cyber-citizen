from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Replace with the path to your WebDriver executable
# Example for Chrome:
webdriver_path = '/path/to/chromedriver'

# Initialize Chrome WebDriver
driver = webdriver.Chrome(executable_path=webdriver_path)

# Open YouTube
driver.get("https://www.youtube.com/")

try:
    # Locate the search input field
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "search_query"))
    )
    
    # Enter the search query (e.g., "music video")
    search_box.send_keys("music video")
    search_box.send_keys(Keys.RETURN)
    
    # Wait for search results to load
    time.sleep(5)
    
    # Click on the first video link
    video_link = driver.find_element(By.CSS_SELECTOR, "#dismissable a#video-title")
    video_link.click()
    
    # Wait for video to start playing (adjust timeout as needed)
    time.sleep(10)
    
    # Get the video duration (for skipping towards the end)
    video_duration_element = driver.find_element(By.CSS_SELECTOR, ".ytp-time-duration")
    video_duration = video_duration_element.text
    
    # Convert video duration to seconds
    minutes, seconds = map(int, video_duration.split(':'))
    total_seconds = minutes * 60 + seconds
    
    # Skip to 80% of the video duration (change percentage as needed)
    skip_time = total_seconds * 0.8
    
    # Use ActionChains to seek to the desired time
    video_player = driver.find_element(By.CSS_SELECTOR, ".html5-video-player")
    actions = ActionChains(driver)
    actions.move_to_element(video_player)
    actions.click_and_hold().perform()
    actions.move_by_offset(skip_time, 0).release().perform()
    
    # Wait for the video to load after seeking (adjust timeout as needed)
    time.sleep(5)
    
    # Pause the video (optional)
    # actions = ActionChains(driver)
    # actions.send_keys(Keys.SPACE).perform()
    
    # Uncomment above lines if you want to pause the video after skipping
    
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser window
    driver.quit()
