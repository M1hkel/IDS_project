import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_data(startlink, deal_type):
    # Selenium setup
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    service = Service("/home/m1hkel/Documents/WebDrivers/chromedriver")  # Replace with your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=options)

    # Cities for reference
    linnad = ["Tartu", "Tallinn", "Pärnu", "Põlva", "Viljandi", "Narva", "Haapsalu", "Rakvere", "Türi", "Paide", "Tapa", "Võru"]

    # Define deal type characteristics
    is_for_sale = "For Sale" if deal_type in [1, 3] else "For Rent"

    try:
        current_url = startlink
        while True:
            driver.get(current_url)

            # Wait until articles are loaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.default"))
            )

            # Get all articles on the current page
            articles = driver.find_elements(By.CSS_SELECTOR, "article.default")

            for index, article in enumerate(articles):
                try:
                    # Refresh the article list in case DOM changed
                    articles = driver.find_elements(By.CSS_SELECTOR, "article.default")
                    article = articles[index]

                    # Determine the type of property
                    if "object-type-house" in article.get_attribute("class"):
                        property_type = "House"
                    elif "object-type-apartment" in article.get_attribute("class"):
                        property_type = "Apartment"
                    else:
                        continue

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
                    town = ""
                    year_built = "N/A"  # Default value if year built is not found
                    for i in linnad:
                        if i in property_title:
                            town = i
                            for row in rows:
                                th_element = row.find_elements(By.TAG_NAME, "th")
                                td_element = row.find_elements(By.TAG_NAME, "td")
                                if th_element and td_element:
                                    key = th_element[0].text.strip()  # Extract header text
                                    value = td_element[0].text.strip()  # Extract corresponding value
                                    data[key] = value

                            # Extract year built if available
                            year_built = data.get("Ehitusaasta", "N/A")

                    # Extract relevant details
                    amount_of_rooms = data.get('Tube', 'N/A')
                    surface_area = data.get('Üldpind', 'N/A')
                    floor = data.get('Korrus/Korruseid', 'N/A')

                    # Save to CSV
                    with open("Data.csv", mode="a", newline="", encoding="utf-8") as file:
                        writer = csv.writer(file)
                        writer.writerow([
                            town,
                            property_price,
                            amount_of_rooms,
                            surface_area,
                            floor,
                            year_built,
                            property_type,
                            is_for_sale
                        ])

                    # Navigate back to the current page
                    driver.get(current_url)

                except Exception as e:
                    print(f"Error processing property {index + 1}: {e}")

            # Check if there is a "Next Page" button
            try:
                next_page = driver.find_element(By.CSS_SELECTOR, "a[rel='next']")
                current_url = next_page.get_attribute("href")  # Update the current URL to the next page
                print(f"Moving to next page: {current_url}")
            except Exception:
                print("No more pages to process.")
                break  # Exit the loop when there are no more pages

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()


# Create or append to the CSV file with a header row if not exists
with open("Data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Town", "Price", "Amount of Rooms", "Surface Area", "Floor/Floors", "Year Built", "Type", "Sale/Rent"])

# Loop through different deal types and paginated URLs
deal_types = [
    (1, "https://www.kv.ee/search?deal_type=1", "https://www.kv.ee/kinnisvara/korterid?start={}"),
    (2, "https://www.kv.ee/search?deal_type=2", "https://www.kv.ee/kinnisvara/korterid_yyr?start={}"),
    (3, "https://www.kv.ee/search?deal_type=3", "https://www.kv.ee/search?deal_type=3&start={}"),
    (4, "https://www.kv.ee/search?deal_type=4", "https://www.kv.ee/kinnisvara/majad_yyr?start={}")
]

for deal_type, base_link, pagination_link in deal_types:
    get_data(base_link, deal_type)
    try:
        count = 50
        while count <= 100000:
            get_data(pagination_link.format(count), deal_type)
            count += 50
    except Exception as e:
        print(f"Pagination ended for deal type {deal_type}: {e}")
