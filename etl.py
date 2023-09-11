import pandas as pd
from io import StringIO
import time

from webdriver_manager.chrome import ChromeDriverManager 
from selenium import webdriver 
options = webdriver.ChromeOptions()
options.add_argument("--headless")
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

class ETL:
    URL = "https://bitcoincharts.com/charts/bitstampUSD#rg60ztgSzm1g10zm2g25zv"

    def __init__(self) -> None:
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 10)

    def extract(self):
        self.driver.get(self.URL)
        
        advanced_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/button[3]")))
        advanced_button.click()

        proceed_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[3]/p[2]/a")))
        proceed_link.click()

        time_period_retroactive_time = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/form/div[2]/select[1]")))
        select = Select(time_period_retroactive_time)
        select.select_by_visible_text('All Data')

        time_period_frequency = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/form/div[2]/select[2]")))
        select = Select(time_period_frequency)
        select.select_by_visible_text('Daily')

        load_raw_data =  self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div[2]/a")))
        load_raw_data.click()

        time.sleep(5)
        table_html = self.driver.find_element(By.XPATH, "/html/body/div[6]/div/div[2]/table").get_attribute('outerHTML')
        
        return pd.read_html(StringIO(table_html))[0]
        

    def transform(self, data):
        pass
    
    def load(self, transformed_data):
        pass
        #file_path = f'{self.SAVE_PATH}{self.city_name}_weather-report_{datetime.now().timestamp()}.csv'
        #transformed_data.to_csv(file_path, index=False)  