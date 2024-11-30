from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Selenium setup
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
service = Service("D:/WebDrivers/chromedriver.exe")  # Replace with your ChromeDriver path
driver = webdriver.Chrome(service=service, options=options)

# Base URL
url = "https://www.kv.ee/search?deal_type=1"
linnad = ["Tartu", "Tallinn", "Pärnu", "Põlva", "Viljandi", "Narva", "Haapsalu", "Rakvere", "Türi", "Paide", "Tapa", "Võru"]

try:
    driver.get(url)

    # Wait until articles are loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.default.object-type-apartment"))
    )

    while True:
        # Get all articles on the current page
        articles = driver.find_elements(By.CSS_SELECTOR, "article.default.object-type-apartment")

        for index, article in enumerate(articles):
            try:
                # Refresh the article list in case DOM changed
                articles = driver.find_elements(By.CSS_SELECTOR, "article.default.object-type-apartment")
                article = articles[index]

                # Extract the URL for the detail page
                relative_url = article.get_attribute("data-object-url")
                if not relative_url:
                    continue

                # Navigate to the article's detail page
                full_url = "https://www.kv.ee" + relative_url
                driver.get(full_url)

                # Wait for the h1 element to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "h1"))
                )

                # Extract the title of the property
                property_title = driver.find_element(By.TAG_NAME, "h1").text

                # Extract the property price
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.price-outer"))
                )
                property_price = driver.find_element(By.CSS_SELECTOR, "div.price-outer").text.strip()

                # Extract additional property details
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.meta-table"))
                )
                rows = driver.find_elements(By.CSS_SELECTOR, "div.meta-table table.table-lined tbody tr")

                # Extract details from the meta table
                data = {}
                linn = ""
                for i in linnad:
                    if i in property_title:
                        linn = i
                        for row in rows:
                            th_element = row.find_elements(By.TAG_NAME, "th")
                            td_element = row.find_elements(By.TAG_NAME, "td")
                            if th_element and td_element:
                                key = th_element[0].text.strip()  # Extract header text
                                value = td_element[0].text.strip()  # Extract corresponding value
                                data[key] = value

                # Print the extracted data
                print(f"\nProperty {index + 1}:")
                print(f"Linn: {linn}")
                print(f"Title: {property_title}")
                print(f"Price: {property_price}")
                print(f"Tube: {data.get('Tube', 'N/A')}")
                print(f"Üldpind: {data.get('Üldpind', 'N/A')}")
                print(f"Korrus: {data.get('Korrus/Korruseid', 'N/A').split('/')[0] if 'Korrus/Korruseid' in data else 'N/A'}")
                print(f"Ehitusaasta: {data.get('Ehitusaasta', 'N/A')}")
                print(f"Omandivorm: {data.get('Omandivorm', 'N/A')}")

                # Navigate back to the main page
                driver.back()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.default.object-type-apartment"))
                )

            except Exception as e:
                print(f"Error processing property {index + 1}: {e}")

        # TODO: Add pagination handling logic here
        break  # Remove this to process multiple pages

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
