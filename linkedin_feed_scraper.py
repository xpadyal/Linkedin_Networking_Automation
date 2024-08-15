from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from langchain_core.prompts import PromptTemplate
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


os.getenv("OPENAI_API_KEY")

llm = OpenAI(temperature=0, max_tokens=250)

def initialize_driver():
    options = Options()
    # Comment out the next line if you want to see the browser UI
    # options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def login_to_linkedin(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    
    email_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    
    email_field.send_keys(username)
    password_field.send_keys(password)
    
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)  # Wait for login to complete

def scrape_feed(driver):
    driver.get("https://www.linkedin.com/feed/")
    time.sleep(5)  # Wait for the feed to load

    posts_elements = driver.find_elements(By.XPATH, '//*[@id="fie-impression-container"]/div[2]/div/div/span/span')  # Adjust XPATH to target post texts
    
    
    # driver.execute_script("window.scrollTo(0, 0);")
    # print("Scrolled back to the top")
    return posts_elements

def comment_on_post(driver, i, text):
    comment_buttons = driver.find_elements(By.XPATH, '//span//div//button')
    print("len of comment buttons:", len(comment_buttons))

    button = comment_buttons[i]
    print("Clicking on comment button")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
    time.sleep(1)
    button.click()
    print("Clicked on comment button")

    time.sleep(2)

    # Locate the comment text box that appears
    comment_box_xpath = "//div[contains(@class, 'ql-editor ql-blank')]"
    try:
        # Wait for the comment box to appear
        comment_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, comment_box_xpath))
        )
        print("Comment box found by XPath")
        
        # Click the comment box to activate it
        comment_box.click()
        time.sleep(1)

        # Send the custom text to the comment box
        comment_box.send_keys(text)
        print(f"Text '{text}' sent to the comment box!")

        time.sleep(2)

        # Locate and click the "Post" button to submit the comment
        post_button_xpath = "//button[contains(@class, 'comments-comment-box__submit-button')]"
        post_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, post_button_xpath))
        )
        print("Post button found")
        post_button.click()
        print("Clicked on Post button")

    except Exception as e:
        print(f"Exception occurred: {e}")
    
    
    
  
    # time.sleep(2)  # Wait for the comment field to appear
    
    # post= driver.find_element(By.XPATH, "//button//span[text()[contains(.,'Post')]]")
    # time.sleep(2)
    # driver.execute_script("arguments[0].click();", post)



def analyze_post_with_llm(post_text, job_query):
    
    prompt_template = PromptTemplate.from_template(
        """I am giving you linkedin posts, you will go through the post and tell weather this is a {job_query} hiring  post or not. Here is the post "{post}", only say yes or no"""
    )

    query = prompt_template.format(post=post_text, job_query= job_query)
    response = llm.invoke(query)
    print(f"Raw response from LLM: {response}")  # Debugging output
    # Ensure the response is parsed correctly if it's a JSON string
   
    answer=response.lower()
        
    is_hiring = 'yes' in answer
    print(f"Is this post hiring for a software engineer? {'Yes' if is_hiring else 'No'}")
    return is_hiring
           



# def main():
#     driver = initialize_driver()
    
#     # Update with your LinkedIn credentials
#     username = "padyal.s@northeastern.edu"
#     password = "Goku@ssj2"
    
#     login_to_linkedin(driver, username, password)
#     posts_elements = scrape_feed(driver)
    
#     for i, post_element in enumerate(posts_elements):
#         post_text = post_element.text
#         if analyze_post_with_llm(post_text):
#             comment_on_post(driver, i)


#     driver.quit()

# if __name__ == "__main__":
#     main()

#//*[@id="fie-impression-container"]//span[@dir="ltr"] for getting posts