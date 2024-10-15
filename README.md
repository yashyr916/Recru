# Recru

Resume and Job Description Similarity Web App🧠


##Overview

Recru is a web application designed to help recruiters efficiently evaluate resumes against a job description (JD) by calculating similarity scores. Recruiters can upload a JD and up to 10 resumes. The app uses Natural Language Processing (NLP) to compare each resume with the JD and rank them based on similarity. The results are displayed in an easy-to-read format with bar charts to help visualize the comparison.

##Features:
-Job Description and Resume Comparison: Upload a job description and up to 10 resumes to get similarity scores between the JD and each resume.
-Visualization: Results are displayed with both a similarity percentage and a bar chart for better understanding.
-Advanced Filtering: Filter resumes based on custom criteria such as minimum similarity score or specific keywords.
-User-Friendly Interface: An attractive and modern UI with animations, icons, and a loading screen for enhanced user engagement.

##Technologies Used
-Backend: Flask (Python-based web framework)
-NLP Processing: SpaCy (for text processing and similarity calculations)
-Data Visualization: Matplotlib (for generating similarity charts)
-Front-end: HTML, CSS (with animations and modern design elements)
-Miscellaneous: Base64 encoding for embedding charts directly in the HTML result page
