from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys



chrome_options = Options()
chrome_options.add_argument("--start-maximized")

def search_query_job(driver, query):
    search = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search"]'))
    )
    search.send_keys(query)
    search.send_keys(Keys.ENTER)

    job_tab = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Jobs"]'))
    )
    job_tab.click()

def scrape_job_listings(driver, num_pages=2):
    job_listings = []
    # driver.get("https://www.linkedin.com/")
    time.sleep(5)
    page = 1
    for _ in range(num_pages):
        time.sleep(10)
        jobs = driver.find_elements(By.XPATH, '//ul//span//strong')
        print(len(jobs))
        for job in jobs:
            try:
                job.click()
                time.sleep(2)

                title = job.find_element(By.XPATH, "//h1//a").text
                print("Job Title:", title)
                company = job.find_element(By.XPATH, "//div[contains(@class, 'job-details-jobs-unified-top-card__company-name')]").text
                print("Company:", company)
                time.sleep(2)
                description = driver.find_element(By.XPATH, '//article').text
                job_listings.append({'Job Title': title, 'Company': company, 'Location': None, 'Job Description': description, 'Apply Link': None})
            except Exception as e:
                print(f"Error while scraping job: {e}")

        try:

            next_page_button = driver.find_element(By.XPATH, "//li[@data-test-pagination-page-btn]//button//span[contains(text(), '2')]")
   
            driver.execute_script("arguments[0].click();", next_page_button)
            time.sleep(5)
            page += 1
        except Exception as e:
            print(f"Error while clicking next page: {e}")
            break
    
    return job_listings

def save_job_listings_to_csv(job_listings, filename='linkdin_Job_data.csv'):
    df = pd.DataFrame(job_listings)
    df.to_csv(filename, index=False)
    print(f"Job listings saved to {filename}")
    return filename