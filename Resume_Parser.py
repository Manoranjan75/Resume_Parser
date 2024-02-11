import streamlit as st
from pdfminer.high_level import extract_text
import re
import nltk

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

# Function to extract names
def extract_names(txt):
    person_names = []
    for sent in nltk.sent_tokenize(txt):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                person_names.append(' '.join(c[0] for c in chunk.leaves()))
    return person_names

# Function to extract phone numbers
PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
def extract_phone_number(resume_text):
    phone = re.findall(PHONE_REG, resume_text)
    if phone:
        number = ''.join(phone[0])
        if resume_text.find(number) >= 0 and len(number) < 16:
            return number
    return None

# Function to extract emails
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
def extract_emails(resume_text):
    return re.findall(EMAIL_REG, resume_text)


def extract_skills(input_text):
    # Define stop words and skills database
    stop_words = set(nltk.corpus.stopwords.words('english'))
    SKILLS_DB = set(["Python", "Java", "C++", "Machine Learning", "Data Analysis", "Data Mining", "Statistics"])
  
    # Tokenize and filter  
    word_tokens = nltk.word_tokenize(input_text)
    filtered_tokens = [w for w in word_tokens if w.lower() not in stop_words]
  
    # Extract n-grams
    bigrams_trigrams = nltk.ngrams(filtered_tokens, 2) 
  
    # Search for matches
    found_skills = []
    for token in filtered_tokens:
        if token.lower() in SKILLS_DB:
            found_skills.append(token)
      
    for ngram in bigrams_trigrams:
        ngram_str = ' '.join(ngram)  # Convert tuple to string
        if ngram_str.lower() in SKILLS_DB:
            found_skills.append(ngram_str)

    return found_skills


# Function to extract education
def extract_education(input_text):
    RESERVED_WORDS = ["university", "college", "school", "degree"]
  
    organizations = []
  
    # Extract organizations
    for sent in nltk.sent_tokenize(input_text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'ORGANIZATION':
                organizations.append(' '.join(c[0] for c in chunk.leaves()))
        
    # Search for matches         
    education = []
    for org in organizations:
        if any(word in org.lower() for word in RESERVED_WORDS):
            education.append(org)

    return education

# Streamlit UI
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
