from seleniumbase import BaseCase

class MyFirstScraper(BaseCase):
    def test_scrape_example(self):
        self.open("https://example.com")
        print("Tytuł strony:", self.get_title())
