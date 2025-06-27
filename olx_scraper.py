import json
from seleniumbase import BaseCase

class OLXScraper(BaseCase):
    def test_scrape_olx_laptops(self):
        # Fraza wyszukiwania
        search_query = "laptop lenovo"
        url = f"https://www.olx.pl/oferty/q-{search_query.replace(' ', '-')}/"

        self.open(url)

        self.wait_for_element('[data-cy="l-card"]', timeout=30)
        offers = self.find_elements('[data-cy="l-card"]')

        # print(f"\nZnaleziono ofert: {len(offers)}\n")

        scraped_data = []

        for offer in offers:
            try:
                title = offer.find_element("css selector", 'div[data-cy="ad-card-title"] h4').text
                price = offer.find_element("css selector", 'p[data-testid="ad-price"]').text
                location = offer.find_element("css selector", 'p[data-testid="location-date"]').text
                
                # print(f"📌 {title} | 💵 {price} | 📍 {location}")

                data = {
                    "title": title,
                    "price": price,
                    "location_date": location
                }

                scraped_data.append(data)

            except Exception as e:
                print("⚠️ Błąd przy parsowaniu ogłoszenia:", e)

            with open("olx_laptops.json", "w", encoding="utf-8") as f:
                json.dump(scraped_data, f, ensure_ascii=False, indent=4)

            print("\n✅ Dane zapisane do pliku olx_laptops.json")
