import streamlit as st
from Sendrequest import generate_message, setup_driver, login, search_query, find_connect_buttons, send_connection_request, click_next_page, save_user_names_to_file
import linkedin_feed_scraper
from LLM import process_csv, convert_csv_to_text, create_pinecone_index_and_store, extract_skills_from_resume, find_relevant_jobs, llm
from ScrapJobListing import scrape_job_listings, save_job_listings_to_csv,search_query_job
from linkedin_feed_scraper import initialize_driver, login_to_linkedin, scrape_feed, analyze_post_with_llm, comment_on_post

# Initialize session state for storing user names if not already present
if 'user_names' not in st.session_state:
    st.session_state.user_names = []

st.title("LinkedIn Auto Connector")

with st.expander("Generate Message with AI"):
    st.header("Generate Message with AI")
    sender_name = st.text_input("Enter sender's name for the message template")
    
    if st.button("Generate Message"):
        if sender_name:
            generated_message = generate_message(sender_name)
            st.session_state.generated_message = generated_message
            st.success("Message template generated successfully.")

with st.expander("Send Connection Requests"):
    st.header("Send Connection Requests")
    email = st.text_input("LinkedIn Email")
    password = st.text_input("LinkedIn Password", type="password")
    query = st.text_input("Search Query")
    max_requests = st.number_input("Max Connection Requests", min_value=1, max_value=100, value=50)
    
    if 'generated_message' not in st.session_state:
        st.session_state.generated_message = "Hi, I'd like to connect with you on LinkedIn."
    
    message_template = st.text_area("Connection Request Message Template", value=st.session_state.generated_message, max_chars=300)
    message_length = len(message_template)

    st.write(f"Character count: {message_length}/300")

    if st.button("Generate with AI"):
        st.experimental_rerun()
    
    if st.button("Start Sending Requests"):
        if email and password and query and max_requests and message_template:
            if message_length <= 300:
                driver = setup_driver()
                login_success = login(driver, email, password)
                if login_success:
                    st.success("Login successful!")
                    total_requests_sent = 0
                    placeholder = st.empty()  # Placeholder for the request counter
                    placeholder.write(f"Total Requests Sent: {total_requests_sent}")
                    search_query(driver, query)
                    while total_requests_sent < max_requests:
                        connect_buttons = find_connect_buttons(driver)
                        for button in connect_buttons:
                            if total_requests_sent >= max_requests:
                                break
                            send_connection_request(driver, button, message_template, st.session_state.user_names)
                            total_requests_sent += 1
                            placeholder.write(f"Total Requests Sent: {total_requests_sent}")
                        if total_requests_sent < max_requests:
                            if not click_next_page(driver):
                                break
                        # time.sleep(3)  # Adjust if necessary
                    st.success(f"Completed sending {total_requests_sent} connection requests.")
                    # driver.quit()
                    file_path = save_user_names_to_file(st.session_state.user_names)
                    with open(file_path, "rb") as file:
                        btn = st.download_button(
                            label="Download Connection Requests List",
                            data=file,
                            file_name="connection_requests.txt",
                            mime="text/plain"
                        )
                else:
                    st.error("Login failed. Please check your credentials.")
            else:
                st.error("Message template exceeds 300 characters.")
        else:
            st.error("Please fill in all the fields.")

    if st.button("Quit"):
        driver.quit()
        st.write("Browser closed.")
        file_path = save_user_names_to_file(st.session_state.user_names)
        with open(file_path, "rb") as file:
            btn = st.download_button(
                label="Download Connection Requests List",
                data=file,
                file_name="connection_requests.txt",
                mime="text/plain"
            )



# Initialize session state for storing user names if not already present
if 'user_names' not in st.session_state:
    st.session_state.user_names = []

st.title("LinkedIn Job Scraper")

with st.expander("Comment on LinkedIn Feed for Hiring Posts"):
    st.header("Scrape LinkedIn Feed")
    email = st.text_input("LinkedIn Email for Scraping", key="scrape_email")
    password = st.text_input("LinkedIn Password for Scraping", type="password", key="scrape_password")
    custom_message = st.text_input("Custom Comment Message", value="Interesting")
        # search = st.text_input("Search Query", key="search_query")
    post_search_query = st.text_input("What kind of hiring post you want to look for?" , key="job-query")
    if st.button("Start Automation"):
        if email and password and custom_message:
            driver = initialize_driver()
            login_to_linkedin(driver, email, password)
            st.write("Logged in successfully!")
            
            posts_elements = scrape_feed(driver)
            st.write(f"Found {len(posts_elements)} posts.")
            
            for i, post_element in enumerate(posts_elements):
                post_text = post_element.text
                st.write(f"Analyzing post {i + 1}: {post_text[:100]}...")
                
                if analyze_post_with_llm(post_text,post_search_query):
                    st.write(f"Post {i + 1} is a hiring post. Commenting...")
                    comment_on_post(driver, i, custom_message)
                    st.write(f"Commented on post {i + 1}.")
                else:
                    st.write(f"Post {i + 1} is not a hiring post.")
            
            driver.quit()
            st.write("Automation completed!")
        else:
            st.error("Please enter both username and password.")

with st.expander("Login and Search Jobs"):
    st.header("Login and Search Jobs")
    st.text("Remember to Zoom out browser window to 25%")

    email = st.text_input("LinkedIn Email" , key="Login-email")
    password = st.text_input("LinkedIn Password", type="password" , key="Login-pass")
    num_pages = st.number_input("Number of Pages to Scrape", min_value=1, max_value=100, value=2)
    search = st.text_input("Search Query", key="search_query")

    if st.button("Start Scraping Jobs list"):
        if email and password:
            driver = setup_driver()
            login_success = login(driver, email, password)
            if login_success:
                st.success("Login successful!")
                search_query_job(driver, search)
                job_listings = scrape_job_listings(driver, num_pages=num_pages)
                driver.quit()
                filename = save_job_listings_to_csv(job_listings)
                st.success("Job listings scraped and saved successfully.")
                st.session_state.filename = filename
            else:
                st.error("Login failed. Please check your credentials.")
        else:
            st.error("Please enter both email and password.")
    
    if 'filename' in st.session_state:
        filename = st.session_state.filename
        
        with open(filename, "rb") as file:
            btn = st.download_button(
                label="Download Job Listings",
                data=file,
                file_name=filename,
                mime="text/csv"
            )
    else:
        st.write("No job listings available. Please scrape job listings first.")



with st.expander("Find Relevant Jobs Based on Resume"):
    st.header("Find Relevant Jobs Based on Resume")
    uploaded_file = st.file_uploader("Upload your resume (PDF format)", type=["docx", "pdf"])
    
    if uploaded_file is not None:
        resumetxt = extract_skills_from_resume(uploaded_file)
        st.write("Extracted Skills:", resumetxt)

        # Process CSV and convert to text
        csv_file_path = "linkdin_Job_data.csv"
        filtered_csv_file_path = "filtered_csv_file.csv"
        structured_text_file_path = "filteredjobtxt.txt"

        process_csv(csv_file_path, filtered_csv_file_path)
        convert_csv_to_text(filtered_csv_file_path, structured_text_file_path)

        # Create Pinecone index and vector store
        docsearch = create_pinecone_index_and_store(structured_text_file_path)

        # Find relevant jobs
        relevant_jobs = find_relevant_jobs(resumetxt, docsearch)
        st.write("Relevant Jobs:", relevant_jobs)

