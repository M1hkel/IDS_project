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

    # Get the first article
    article = driver.find_element(By.CSS_SELECTOR, "article.default.object-type-apartment")
    relative_url = article.get_attribute("data-object-url")
    if relative_url:
        # Navigate to the article's detail page
        full_url = "https://www.kv.ee" + relative_url
        driver.get(full_url)

        # Wait for the h1 element to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        # Extract the text from the <h1> tag
        property_title = driver.find_element(By.TAG_NAME, "h1").text
        print(f"Property Title: {property_title}")

        # Wait for the meta table to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.meta-table"))
        )

        # Locate the table rows inside the meta table
        rows = driver.find_elements(By.CSS_SELECTOR, "div.meta-table table.table-lined tbody tr")

        # Extract and print data points from the rows
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

        print(linn)
        print(data["Tube"])
        print(data["Üldpind"])
        print(data["Korrus/Korruseid"].split("/")[0])
        print(data["Ehitusaasta"])
        print(data["Omandivorm"])

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
