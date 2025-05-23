from bs4 import BeautifulSoup
import random
import time
import undetected_chromedriver as uc
import pandas as pd
from encrypt import Encrypt


class TRTScraper:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:101.0) Gecko/20100101 Firefox/101.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0.3 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edge/96.0.1054.62",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 OPR/80.0.4170.72",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; ASL 1.0; .NET4.0E; .NET4.0C; InfoPath.3) like Gecko",
            "Mozilla/5.0 (Linux; Android 10; Pixel 4 XL Build/QD1A.190805.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Android 10; Mobile; rv:85.0) Gecko/85.0 Firefox/85.0",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.12.388 Version/12.17",
            "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.0 Chrome/73.0.3683.90 Mobile Safari/537.36",
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)"
        ]

    def human_typing(self, element, text):
        """Simulate human typing"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.3))

    def setup_driver(self):
        """Set up undetected Chrome driver with random user agent"""
        user_agent = random.choice(self.user_agents)
        print("Using User-Agent:", user_agent)
        options = uc.ChromeOptions()
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = uc.Chrome(options=options)

    def login(self):
        """Log into the TRT website"""
        self.driver.get('https://www.usatrt.com/app/login.aspx?ReturnUrl=%2Fapp%2FUserPages%2FPurchase.aspx#/purchases')
        time.sleep(random.uniform(1, 3))
        self.driver.maximize_window()

        email_input = self.driver.find_element(by="xpath", value='//*[@id="Login1_txtName"]')
        pass_input = self.driver.find_element(by="xpath", value='//*[@id="Login1_txtPassword"]')
        login_button = self.driver.find_element(by="xpath", value='//*[@id="Login1_btnLogin"]')

        self.human_typing(email_input, self.email)
        time.sleep(random.uniform(0.5, 1.5))
        self.human_typing(pass_input, self.password)
        time.sleep(random.uniform(0.5, 1.5))
        login_button.click()

    def navigate_vehicle_list(self):
        """Navigate to vehicle list and adjust view settings"""
        time.sleep(random.uniform(2, 4))
        self.driver.get("https://www.usatrt.com/app/UserPages/vehicleList.aspx")
        time.sleep(1)

        self.driver.find_element(by="xpath", value='//*[@id="ctl00_BodyHolder_ddlLoadStatus"]').click()
        time.sleep(0.5)
        self.driver.find_element(by="xpath", value='//*[@id="ctl00_BodyHolder_ddlLoadStatus"]/option[5]').click()
        time.sleep(1)
        self.driver.find_element(by="xpath", value='//*[@id="ctl00_BodyHolder_ddlShow"]').click()
        time.sleep(0.5)
        self.driver.find_element(by="xpath", value='//*[@id="ctl00_BodyHolder_ddlShow"]/option[3]').click()
        time.sleep(4)

    def extract_links(self):
        """Extract JavaScript pagination links from the page"""
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        table = soup.find('table', id='ctl00_BodyHolder_myDataGrid_VIT')
        rows = table.find_all('td', attrs={"colspan": True})

        links = []
        for row in rows:
            for a in row.find_all('a', href=True):
                links.append(a['href'])
        return links

    def extract_table_data(self):
        """Extract table data from current page"""
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        table = soup.find('table', id='ctl00_BodyHolder_myDataGrid_VIT')
        data = []

        for row in table.find_all('tr')[1:-1]:  # skip header and footer
            data.append([td.text.strip() for td in row.find_all('td')])
        return data

    def scrape_all_data(self):
        """Main scraping routine"""
        all_data = []

        # Initial page data
        all_data += self.extract_table_data()

        # Extract and loop through multiple pages
        link_groups = [self.extract_links()]
        print(link_groups)
        for group_index in range(3):  # You used 3 rounds of link clicking
            if group_index < len(link_groups):
                new_links = []
                for link in link_groups[-1][group_index:]:
                    self.driver.execute_script(link)
                    time.sleep(random.uniform(1, 2.5))
                    all_data += self.extract_table_data()
                    new_links = self.extract_links()
                link_groups.append(new_links)

        return all_data

    def export_to_excel(self, data, filename="TRT CARS.xlsx"):
        """Export data to Excel"""
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        table = soup.find('table', id='ctl00_BodyHolder_myDataGrid_VIT')
        headers = [th.text.strip() for th in table.find_all('tr')[0].find_all('th')]
        headers = [h for h in headers if h != ""]

        df = pd.DataFrame(data, columns=headers)
        df.drop_duplicates(inplace=True)
        df.to_excel(filename, index=False)
        print(f"Data saved to {filename}")
        print(df)

    def run(self):
        """Run the scraper"""
        try:
            self.setup_driver()
            self.login()
            self.navigate_vehicle_list()
            all_data = self.scrape_all_data()
            self.export_to_excel(all_data)
            input("Enter something to finish...")
        except Exception as e:
            print("Error:", e)
        finally:
            if self.driver:
                self.driver.quit()


if __name__ == "__main__":
    main = Encrypt()
    scraper = TRTScraper(email=main.decrypt_message(main.email()), password=main.decrypt_message(main.password()))
    scraper.run()


if __name__ == "__main__":
    main = MainClass()
    scraper = TRTScraper(email=main.decrypt_message(main.email()), password=main.decrypt_message(main.password()))
    scraper.run()
