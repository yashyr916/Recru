from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)


# Function to read file content
def read_file_content(file):
    content = file.read().decode('utf-8', errors='ignore')
    return content

# Function to calculate similarity
def calculate_similarity(jd_text, resumes):
    documents = [jd_text] + resumes
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Calculate cosine similarity for job description vs resumes
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    return similarity

# Function to create visualizations and return as Base64 strings
def create_visualizations(results):
    # Bar chart for similarity scores
    plt.figure(figsize=(10, 5))
    plt.barh(results['Resume'], results['Similarity (%)'], color='skyblue')
    plt.xlabel('Similarity Percentage')
    plt.title('Resume Similarity to Job Description')
    plt.grid(axis='x')
    plt.tight_layout()

    # Save bar chart to a BytesIO object and encode to Base64
    bar_img = BytesIO()
    plt.savefig(bar_img, format='png')
    plt.close()
    bar_img.seek(0)
    bar_img_b64 = base64.b64encode(bar_img.getvalue()).decode()

    # Pie chart for similarity distribution
    fig = px.pie(results, values='Similarity (%)', names='Resume', title='Resume Similarity Distribution', color='Resume')
    
    # Save pie chart to a BytesIO object and encode to Base64
    pie_img = BytesIO()
    pio.write_image(fig, pie_img, format='png')
    pie_img.seek(0)
    pie_img_b64 = base64.b64encode(pie_img.getvalue()).decode()

    return bar_img_b64, pie_img_b64

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    job_description = request.files['job_description']
    resumes = request.files.getlist('resumes')

    # Read job description
    jd_text = read_file_content(job_description)
    
    # Read resumes
    resume_texts = []
    for resume in resumes:
        resume_text = read_file_content(resume)
        resume_texts.append(resume_text)

    # Calculate similarity
    similarity_scores = calculate_similarity(jd_text, resume_texts)

    # Prepare results
    results = pd.DataFrame({
        'Resume': [resume.filename for resume in resumes],
        'Similarity (%)': similarity_scores * 100  # Convert to percentage
    })

    # Sort results in ascending order
    results = results.sort_values(by='Similarity (%)', ascending=True)

    # Create visualizations
    bar_img_b64, pie_img_b64 = create_visualizations(results)

    # Return results to the user
    return render_template('results.html', tables=[results.to_html(classes='data', index=False)],bar_img=bar_img_b64, pie_img=pie_img_b64)

def clean_resume_text(text):
    # Remove empty lines and unnecessary spaces
    return " ".join(text.split()).replace("\n", " ")

if __name__ == '__main__':
    app.run(debug=True)
