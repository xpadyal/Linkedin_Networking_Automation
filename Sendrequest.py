import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_cohere import ChatCohere

load_dotenv()

os.getenv("COHERE_API_KEY")

def generate_message(sender_name):
    
    model = ChatCohere(model="command-r-plus", max_tokens=None, temperature=0)
    prompt = PromptTemplate.from_template("Write a very short message for sending a connection request on linkedin, the sender is {input} and don't add Hi Recepient Name, only the message without any fillin the blanks. Just the sender's name")
    chain = prompt | model
    msg = chain.invoke(input=sender_name)
    return msg.content

def setup_driver():
    options = Options()
    # Comment out the next line if you want to see the browser UI
    # options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def login(driver, email, password):
    try:
        # Open LinkedIn homepage
        driver.get("https://www.linkedin.com")

        # Click the "Sign In" button
        sign_in_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sign in"))
        )
        sign_in_button.click()
        
        # Enter email
        email_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        email_field.send_keys(email)

        # Enter password
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        
        # Click the login button
        login_button = driver.find_element(By.XPATH, '//*[@type="submit"]')
        login_button.click()

        # Wait for the login to complete
        search = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search"]'))
        )
        return True
        
    except Exception as e:
        print(f"An error occurred during login: {e}")
        return False

def search_query(driver, query):
    search = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search"]'))
    )
    search.send_keys(query)
    search.send_keys(Keys.ENTER)

    people_tab = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="People"]'))
    )
    people_tab.click()

def find_connect_buttons(driver):
    return WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.XPATH, '//button[.//text()[contains(.,"Connect")]]'))
    )

def send_connection_request(driver, button, message_template, user_names):
    try:
        time.sleep(1)  # Small sleep to ensure smooth scrolling
        button.click()
        print("Clicked on Connect button")

        time.sleep(2)
        # Extract and store the user's name
        user_name_element = driver.find_element(By.XPATH, "//span[@class='flex-1']//strong")
        user_name = user_name_element.text
        user_names.append(user_name)

        time.sleep(2)

    

        add_note_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[.//text()[contains(.,"Add a note")]]'))
        )
        add_note_button.click()

        time.sleep(2)

        note_textarea = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//textarea[@name="message"]'))
        )
        note_textarea.send_keys(message_template)

        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[.//text()[contains(.,"Send")]]'))
        )
        send_button.click()
        print("Sent connection request")

    except Exception as e:
        print(f"An error occurred while sending a connection request: {e}")

        


def click_next_page(driver):
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Next")]'))
        )
        next_button.click()
        return True
    except Exception as e:
        print(f"An error occurred while navigating to the next page: {e}")
        return False

def save_user_names_to_file(user_names, file_path='connection_requests.txt'):
    with open(file_path, 'w') as f:
        for name in user_names:
            f.write(name + '\n')
    return file_path