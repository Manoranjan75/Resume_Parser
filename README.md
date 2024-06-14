# Resume Parser

This repository contains a Resume Parser application built using Streamlit. The application allows users to upload a resume in PDF format and extract various information such as names, phone numbers, emails, skills, and education details from the uploaded resume.

## Features

- Extracts text from PDF resumes.
- Identifies and extracts names.
- Extracts phone numbers using regular expressions.
- Extracts email addresses using regular expressions.
- Identifies and extracts skills from a predefined skills database.
- Identifies and extracts education details by recognizing organizational names associated with education.

## Installation

To run the Resume Parser application, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/resume-parser.git
    cd resume-parser
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Download NLTK data:
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
    nltk.download('stopwords')
    ```

## Usage

To run the application, use the following command:
```bash
streamlit run app.py
```

### Application Interface

1. **Upload a Resume (PDF)**: Upload a PDF file containing the resume.
2. **Extracted Names**: Displays the extracted names found in the resume.
3. **Extracted Phone Number**: Displays the extracted phone number found in the resume.
4. **Extracted Emails**: Displays the extracted email addresses found in the resume.
5. **Extracted Skills**: Displays the extracted skills found in the resume.
6. **Extracted Education**: Displays the extracted education details found in the resume.

## Code Overview

### Function to Extract Text from PDF
```python
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)
```
This function uses `pdfminer` to extract text from a given PDF file.

### Function to Extract Names
```python
def extract_names(txt):
    person_names = []
    for sent in nltk.sent_tokenize(txt):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                person_names.append(' '.join(c[0] for c in chunk.leaves()))
    return person_names
```
This function uses NLTK to identify and extract names from the text.

### Function to Extract Phone Numbers
```python
PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
def extract_phone_number(resume_text):
    phone = re.findall(PHONE_REG, resume_text)
    if phone:
        number = ''.join(phone[0])
        if resume_text.find(number) >= 0 and len(number) < 16:
            return number
    return None
```
This function uses a regular expression to identify and extract phone numbers from the text.

### Function to Extract Emails
```python
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
def extract_emails(resume_text):
    return re.findall(EMAIL_REG, resume_text)
```
This function uses a regular expression to identify and extract email addresses from the text.

### Function to Extract Skills
```python
def extract_skills(input_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    SKILLS_DB = set(["Python", "Java", "C++", "Machine Learning", "Data Analysis", "Data Mining", "Statistics"])
    
    word_tokens = nltk.word_tokenize(input_text)
    filtered_tokens = [w for w in word_tokens if w.lower() not in stop_words]
    
    bigrams_trigrams = nltk.ngrams(filtered_tokens, 2)
    
    found_skills = []
    for token in filtered_tokens:
        if token.lower() in SKILLS_DB:
            found_skills.append(token)
    
    for ngram in bigrams_trigrams:
        ngram_str = ' '.join(ngram)
        if ngram_str.lower() in SKILLS_DB:
            found_skills.append(ngram_str)
    
    return found_skills
```
This function identifies and extracts skills from the text by comparing against a predefined skills database.

### Function to Extract Education
```python
def extract_education(input_text):
    RESERVED_WORDS = ["university", "college", "school", "degree"]
    
    organizations = []
    for sent in nltk.sent_tokenize(input_text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'ORGANIZATION':
                organizations.append(' '.join(c[0] for c in chunk.leaves()))
    
    education = []
    for org in organizations:
        if any(word in org.lower() for word in RESERVED_WORDS):
            education.append(org)
    
    return education
```
This function identifies and extracts educational institutions from the text by looking for specific keywords.

### Streamlit UI
```python
def main():
    st.title("Resume Parser")
    uploaded_file = st.file_uploader("Upload a resume (PDF)", type="pdf")
    if uploaded_file is not None:
        resume_text = extract_text_from_pdf(uploaded_file)
        
        st.subheader("Extracted Names")
        names = extract_names(resume_text)
        if names:
            for name in names:
                st.write(name)
        else:
            st.write("No names found.")

        st.subheader("Extracted Phone Number")
        phone_number = extract_phone_number(resume_text)
        if phone_number:
            st.write(phone_number)
        else:
            st.write("No phone number found.")

        st.subheader("Extracted Emails")
        emails = extract_emails(resume_text)
        if emails:
            for email in emails:
                st.write(email)
        else:
            st.write("No emails found.")

        st.subheader("Extracted Skills")
        skills = extract_skills(resume_text)
        if skills:
            for skill in skills:
                st.write(skill)
        else:
            st.write("No skills found.")

        st.subheader("Extracted Education")
        education = extract_education(resume_text)
        if education:
            for edu in education:
                st.write(edu)
        else:
            st.write("No education found.")

if __name__ == "__main__":
    main()
```
This function defines the Streamlit user interface for the Resume Parser application.
