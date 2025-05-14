from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
from dotenv import load_dotenv
import requests
import time
import os

load_dotenv()

class SiteScraper:
    def __init__(self, headless: bool = True, wait_time = 5):
        """
        Initialize the SiteScraper with the path to ChromeDriver
        :param chrome_driver_path: Path to the ChromeDriver executable
        :param headless: Run the browser in headless mode if True
        """
        self.wait_time = wait_time
        try:
            self.service = Service(os.environ.get("CHROME_DRIVER_PATH"))
            self.chrome_options = ChromeOptions()

            if headless:
                self.chrome_options.add_argument("--headless")
                self.chrome_options.add_argument("--disable-gpu")
                self.chrome_options.add_argument("--disable-dev-shm-usage")
                self.chrome_options.add_argument("--window-size=1920,1080")
                self.chrome_options.add_argument("--no-sandbox")
                self.chrome_options.add_argument("--disable-extensions")
                self.chrome_options.add_argument("--disable-infobars")
                self.chrome_options.add_argument("--disable-logging")
                self.chrome_options.add_argument("--disable-background-networking")
                self.chrome_options.add_argument("--disable-sync")
                self.chrome_options.add_argument("--metrics-recording-only")
                self.chrome_options.add_argument("--mute-audio")
                self.chrome_options.add_argument("--remote-debugging-port=9222")


            self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        except FileNotFoundError:
            print("The ChromeDriver executable was not found. Is it installed and accessible in PATH?")
            quit()
        except Exception as e:
            print(f"An unknown error occurred: {e}")
            quit()

    def get_page_source(self, url) -> str:
        """
        Get the page source of the given URL
        :param url: The URL of the page to scrape
        :param wait_time: The time to wait for the page to load (for JavaScript)
        """
        try:
            self.driver.get(url)
        except Exception as e:
            print(f"An error occurred while trying to get the page source: {e}")
            return ""
        if self.wait_time > 0:
            time.sleep(self.wait_time)
        return self.driver.page_source

    def close(self):
        """
        Close the WebDriver
        """
        self.driver.quit()
        self.service.stop()
        print("WebDriver closed successfully")


def download_site_as_html(url: str, timeout: int = 10, response_encoding=None) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        if response_encoding:
            response.encoding = response_encoding
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return ""
