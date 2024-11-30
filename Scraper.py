import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Selenium setup with realistic user-agent
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--disable-usb")
options.add_argument("--log-level=3")
service = Service("D:/WebDrivers/chromedriver.exe")  # Replace with your ChromeDriver path
driver = webdriver.Chrome(service=service, options=options)

# Base URL
url = "https://www.kv.ee/search?deal_type=1"

try:
    driver.get(url)

    # Wait for the "Just a moment..." challenge to pass
    time.sleep(10)  # Adjust based on how long the challenge takes

    # Debug: Print the loaded page source
    print("Page Source:\n", driver.page_source[:2000])  # Print first 2000 characters for debugging

    # Use WebDriverWait to ensure elements are loaded
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.default.object-type-apartment"))
        )
        articles = driver.find_elements(By.CSS_SELECTOR, "article.default.object-type-apartment")
    except Exception as e:
        print("Error: Articles did not load dynamically:", e)
        articles = []

    if not articles:
        print("No articles found. Trying a broader selector...")
        # Try a broader selector to debug
        articles = driver.find_elements(By.CSS_SELECTOR, "article")
        print(f"Found {len(articles)} articles with broader selector.")

    # Process articles if any are found
    for i, article in enumerate(articles[:5]):  # Limit to first 5 articles for demo
        try:
            relative_url = article.get_attribute("data-object-url")
            if relative_url:
                full_url = "https://www.kv.ee" + relative_url
                print(f"Article {i + 1}: {full_url}")
        except Exception as e:
            print(f"Error processing article {i + 1}: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
