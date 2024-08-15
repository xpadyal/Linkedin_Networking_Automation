import random
import json

# Sample data for random generation
skills_pool = [
    "Python", "Machine Learning", "Data Analysis", "JavaScript", "React", 
    "Web Development", "SQL", "Database Management", "ETL", "Data Engineering",
    "Java", "C++", "Cloud Computing", "AWS", "Docker", "Kubernetes", "Node.js",
    "Cybersecurity", "Penetration Testing", "Networking", "DevOps", "UI/UX Design",
    "Project Management", "Agile", "Scrum", "R", "TensorFlow", "Natural Language Processing"
]

job_recommendations_pool = [
    "Data Scientist at Company X - Apply machine learning techniques to extract insights from large datasets.",
    "AI Engineer at Startup Y - Develop and deploy AI models for real-time decision-making.",
    "Senior Frontend Developer at Company Z - Lead the development of modern web applications using React.",
    "Full Stack Developer at Startup A - Work on both frontend and backend technologies to build scalable web applications.",
    "Database Engineer at Corporation B - Design and maintain database systems to ensure optimal performance.",
    "Data Warehouse Architect at Firm C - Develop and manage data warehousing solutions for large-scale data analytics.",
    "DevOps Engineer at Enterprise D - Streamline CI/CD pipelines and automate infrastructure management.",
    "Cybersecurity Analyst at Security Inc. - Perform penetration testing and vulnerability assessments to secure systems.",
    "Cloud Architect at Tech Corp - Design and implement scalable cloud infrastructure using AWS.",
    "UI/UX Designer at Design Studio E - Create intuitive user interfaces and enhance user experiences.",
    "Project Manager at Organization F - Lead projects from conception to completion using Agile methodologies.",
    "Software Engineer at Company G - Develop high-performance software solutions in a collaborative environment."
]

# Function to create random skill sets and experience
def generate_entry():
    num_skills = random.randint(3, 5)
    skills = random.sample(skills_pool, num_skills)
    experience_years = random.randint(1, 10)
    experience = f"{experience_years} years as a {random.choice(['Developer', 'Engineer', 'Analyst', 'Designer', 'Manager'])}"

    num_recommendations = random.randint(1, 3)
    job_recommendations = random.sample(job_recommendations_pool, num_recommendations)

    return {
        "messages": [
            {"role": "system", "content": "This is a job recommendation chatbot."},
            {"role": "user", "content": f"My skills are {', '.join(skills)} and I have {experience}."},
            {"role": "assistant", "content": f"Based on your skills and experience, here are some job recommendations: {', '.join(job_recommendations)}"}
        ]
    }

# Generate 100 entries
with open('job_recommendation_dataset.jsonl', 'w') as f:
    for _ in range(100):
        entry = generate_entry()
        json_line = json.dumps(entry)
        f.write(json_line + '\n')

print("Dataset generated and saved as 'job_recommendation_dataset.jsonl'.")
