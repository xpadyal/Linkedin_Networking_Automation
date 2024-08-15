# LinkedIn Automation Tool

## Overview

The LinkedIn Automation Tool is designed to streamline networking, job searching, and professional communication on LinkedIn by leveraging automation and AI technologies. This tool helps users automate connection requests, scrape and analyze LinkedIn feeds, and provides job recommendations based on the user's resume.

## Key Features

### 1. Automated Connection Requests
- **Functionality:** Automates the process of sending LinkedIn connection requests, including an "Add a Note" feature for personalized messages.
- **AI-Driven Template Generation:** Generate custom connection message templates using OpenAI's language model or input your own templates.
- **Downloadable List:** Users can download a list of names to whom connection requests were sent.

### 2. Post Scraping and Commenting
- **Feed Scraping:** Scrapes the LinkedIn feed to identify posts related to job openings or hiring.
- **AI-Powered Decision Making:** Uses a Large Language Model (LLM) to determine whether a post is hiring-related.
- **Automated Comments:** Automatically comments on identified posts, helping users engage with job opportunities.

### 3. Job List Scraping and AI-Based Recommendations
- **Job Scraping:** Scrapes job listings from LinkedIn's job section.
- **Resume Analysis:** Upload a resume, and the tool uses AI to match relevant job postings to the user's skills and experience.
- **RAG and Vector Stores:** Utilizes Pinecone for storing and retrieving vectorized job and resume data, enhancing the relevance of job recommendations.

## Technologies Used
- **Python:** Backend logic and automation.
- **Langchain:** Manages AI model workflows.
- **Streamlit:** Interactive user interface.
- **Selenium:** Web automation and data scraping.
- **Pandas:** Data manipulation and processing.
- **OpenAI:** AI-driven message generation and job relevance analysis.
- **Pinecone:** Storage and retrieval of vectorized data in the RAG pipeline.

## Evaluation Metrics

| Metric                                      | Current Value | Target Value |  |
|---------------------------------------------|---------------|--------------
| Accuracy of Job Recommendations             | 95%         | 95%          
| User Engagement and Response Rates          | 75%        | 80%          
| Processing Time for Data Scraping and Analysis | 5min MAX        | Depends on usage     

### Methods to Improve Metrics
- **AI Model Enhancement:** Continuously fine-tuned the AI models for better job recommendations and message personalization.
- **Optimized Data Structures:** Ensured job listings are well-structured to avoid mixed or confusing information.

## Deployment
- **Deployment Environment:** Deployable on cloud platforms such as AWS.
- **CI/CD Pipelines:** Implemented using tools like Docker and Jenkins for continuous updates.

## Future Work

### Extensions
- Integrate additional social media platforms for broader networking capabilities.
- Develop a mobile version of the tool for accessibility on the go.

### Long-term Vision
- Expand the tool to support various industries and roles.
- Collaborate with job search platforms to enhance the job recommendation engine.

## Conclusion

The LinkedIn Automation Tool combines automation, AI, and data analysis to enhance professional networking and job searching. It reduces manual effort, improves interaction quality, and provides valuable insights for career advancement, showcasing the practical applications of advanced technologies in real-world scenarios.

## Getting Started

### Prerequisites
- Python 3.x
- Selenium
- Streamlit
- Pandas
- Langchain
- OpenAI API Key
- Pinecone API Key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/linkedin-automation-tool.git

2. pip install -r requirements.txt
3. streamlit run main.py

### Contact Us
Github: github.com/xpadyal
linkedin:linkedin.com/in/sahil-padyal
email: padyal.s@northeastern.edu

