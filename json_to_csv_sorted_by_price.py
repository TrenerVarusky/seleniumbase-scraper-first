import json
import csv
import re

# Wczytaj dane z pliku JSON
with open("olx_laptopsALL.json", "r", encoding="utf-8") as f:
    data = json.load(f)

cleaned_data = []

for offer in data:
    try:
        # Wyciągnij liczbę z ceny, np. "1 499 zł" -> 1499
        price_text = offer["price"]
        price_num = int(re.sub(r"[^\d]", "", price_text))
        
        cleaned_data.append({
            "title": offer["title"],
            "price": price_num,
            "location_date": offer["location_date"],
            "link": offer.get("link", "")  # jeśli nie ma klucza 'link', da pusty
        })

    except Exception as e:
        # Pomijaj oferty z błędną ceną
        continue

# Posortuj po cenie rosnąco
sorted_data = sorted(cleaned_data, key=lambda x: x["price"])

# Zapisz do pliku CSV z kolumną link
with open("olx_sorted_by_price.csv", "w", encoding="utf-8", newline="") as csvfile:
    fieldnames = ["title", "price", "location_date", "link"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in sorted_data:
        writer.writerow(row)

print(f"✅ Zapisano {len(sorted_data)} ogłoszeń do pliku 'olx_sorted_by_price.csv'")
