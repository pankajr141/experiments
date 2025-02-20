from selenium import webdriver
from fake_useragent import UserAgent

class GoogleSearchNewsURLExtractor:
    """Extracts news article URLs from Google search results based on a keyword and site."""

    def __init__(self, keyword, news_domain, user_agent=None):
        """Initialize with the search keyword and the target newspaper URL."""
        self.keyword = keyword
        self.news_domain = news_domain
        self.urls = []  # List to store extracted URLs

        # Prepare the search term for Google
        self.search_term = f"'{self.keyword}' site:{self.news_domain}"
        self.search_url = f"https://www.google.com/search?q={'+'.join(self.search_term.split())}"

        # Set up the web driver options
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode (no UI)
        options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
        options.add_argument("--incognito")  # Open in incognito mode
        options.add_argument("--no-sandbox")
        
        # Adding fake agents, else google will block the request
        if not user_agent:
            ua = UserAgent()
            user_agent = ua.random
        self.user_agent = user_agent
        options.add_argument(f"user-agent={self.user_agent}")

        # Start the web driver
        driver = webdriver.Chrome(options=options)
        driver.get(self.search_url)
        
        self.returned_url = driver.current_url

        def _keyword_present_in_url(url, keyword):
            if not list(filter(lambda x: x in url, keyword.split())):
                return
            return url
    
        try:
            # Find and collect all news article links on the current page
            links = driver.find_elements("xpath", "//div[@class='yuRUbf']/div/span/a")
            links = driver.find_elements("xpath", "//a")
            url_list = [link.get_attribute("href") for link in links]
            
            # Custom code
            url_list = list(filter(lambda x: x and news_domain in x, url_list))
            url_list = [url[url.find(news_domain):] for url in url_list]

            # verify that URL must contain keyword
            url_list = list(filter(lambda url: _keyword_present_in_url(url, keyword), url_list))

            # Filter out unwanted URLs (e.g., PDFs or XMLs) and remove duplicates
            url_list = list(dict.fromkeys(url_list))
            self.urls = [url for url in url_list if ".pdf" not in url and ".xml" not in url]

        except Exception as e:
            raise ValueError(f"An error occurred during the search: {e}")

        finally:
            driver.quit()  # Ensure the driver is closed at the end

if __name__ == "__main__":
    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) GSA/343.0.695551749 Mobile/15E148 Safari/604.1"
    google = GoogleSearchNewsURLExtractor(keyword='tata motors', news_domain='https://www.businesstoday.in/', user_agent=user_agent)   
    print(f"search_url: {google.search_url}")
    print(f"returned_url: {google.returned_url}")
    print(f"urls: {google.urls}")
