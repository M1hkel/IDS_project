from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Selenium setup
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-usb")
service = Service("D:/WebDrivers/chromedriver.exe")  # Replace with the path to your ChromeDriver
driver = webdriver.Chrome(service=service, options=options)

# URL of the website
base_url = "https://www.kv.ee"
url = "https://www.kv.ee/search?deal_type=1"

try:
    driver.get(url)
    driver.implicitly_wait(10)

    # Find all the listings using the CSS selector
    listings = driver.find_elements(By.CSS_SELECTOR, "article.default.object-type-apartment")

    if not listings:
        print("No listings found. Verify your CSS selector.")
    else:
        print(f"Found {len(listings)} listings.")

    # Loop through each listing
    for i, listing in enumerate(listings[:5]):  # Limit to the first 5 listings for demonstration
        try:
            # Extract the relative URL from the `data-object-url` attribute
            object_url = listing.get_attribute("data-object-url")
            print(object_url)
            if object_url:
                # Construct the full URL
                full_url = base_url + object_url
                print(f"Listing {i + 1} URL: {full_url}")

                # Navigate to the full URL
                driver.get(full_url)

                # Wait for the detail page to load
                driver.implicitly_wait(5)

                # Scrape more data on the detail page if necessary
                print(f"  Detail page title: {driver.title}")

                # Go back to the main page
                driver.get(url)
                driver.implicitly_wait(5)

                # Recollect listings since the DOM is reloaded
                listings = driver.find_elements(By.CSS_SELECTOR, "article.default.object-type-apartment")
        except Exception as e:
            print(f"Error processing listing {i + 1}: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
