import pandas as pd
import matplotlib.pyplot as plt
import re

data = pd.read_csv("Data.csv")

apartments_for_sale = data[(data["Type"] == "Apartment") & (data["Sale/Rent"] == "For Sale")]

def clean_price(price):
    try:
        cleaned_price = re.findall(r'\d+\s?\d*', price)
        if cleaned_price:
            return float(cleaned_price[0].replace(" ", ""))
        return None
    except Exception as e:
        print(f"Error cleaning price: {price} - {e}")
        return None

apartments_for_sale["Price"] = apartments_for_sale["Price"].apply(clean_price)

apartments_for_sale = apartments_for_sale.dropna(subset=["Price"])

average_prices = apartments_for_sale.groupby("Town")["Price"].mean()

plt.figure(figsize=(10, 6))
average_prices.sort_values().plot(kind="bar", color="skyblue")
plt.title("Average Apartment Prices by Location (For Sale)", fontsize=16)
plt.xlabel("Location", fontsize=12)
plt.ylabel("Average Price (€)", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.show()
