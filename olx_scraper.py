import csv
import re
from seleniumbase import BaseCase

class OLXScraper(BaseCase):
    def test_scrape_olx_laptops(self):
        search_query = "laptop lenovo"
        base_url = f"https://www.olx.pl/oferty/q-{search_query.replace(' ', '-')}/"
        page = 1
        all_data = []
        last_titles = set()

        while True:
            url = base_url if page == 1 else f"{base_url}?page={page}"
            print(f"\n🌐 Strona {page}: {url}")
            self.open(url)

            try:
                self.wait_for_element('[data-cy="l-card"]', timeout=10)
            except Exception:
                print("❌ Brak wyników lub koniec stron.")
                break

            offers = self.find_elements('[data-cy="l-card"]')
            if not offers:
                print("❌ Brak ogłoszeń na stronie.")
                break

            current_titles = set()
            page_data = []

            for offer in offers:
                try:
                    title = offer.find_element(
                        "css selector", 'div[data-cy="ad-card-title"] h4'
                    ).text

                    price_text = offer.find_element(
                        "css selector", 'p[data-testid="ad-price"]'
                    ).text
                    price_num = int(re.sub(r"[^\d]", "", price_text))

                    location = offer.find_element(
                        "css selector", 'p[data-testid="location-date"]'
                    ).text

                    link_element = offer.find_element(
                        "css selector", 'a[href^="/d/oferta/"]'
                    )
                    
                    href = link_element.get_attribute("href")
                    link = href if href.startswith("http") else f"https://www.olx.pl{href}"

                    current_titles.add(title)

                    page_data.append({
                        "title": title,
                        "price": price_num,
                        "location_date": location,
                        "link": link
                    })

                except Exception as e:
                    print("⚠️ Błąd przy ogłoszeniu:", e)

            if current_titles == last_titles:
                print("🚫 Powtórzone dane — koniec stron.")
                break

            last_titles = current_titles
            all_data.extend(page_data)
            print(f"✅ Zebrano {len(page_data)} ogłoszeń z tej strony.")
            page += 1

        # Sortuj po cenie
        sorted_data = sorted(all_data, key=lambda x: x["price"])

        # Zapisz do CSV
        with open("olx_laptops_sorted.csv", "w", encoding="utf-8", newline="") as csvfile:
            fieldnames = ["title", "price", "location_date", "link"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in sorted_data:
                writer.writerow(row)

        print(f"\n✅ Zapisano {len(sorted_data)} ogłoszeń do olx_laptops_sorted.csv")
