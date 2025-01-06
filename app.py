import streamlit as st
import base64
from AIRecruitmentAssistant.resume_parser import skills, document_loader, summarizer, fit_or_not, name_from_resume
from AIRecruitmentAssistant.email_generator import success_email,apology_email

def main():
  st.title("AI Recruitment System")
  # Sidebar content
  with st.sidebar:
    email = st.text_input("Enter the Email", "")
    password = st.text_input("Enter the password", "",type = 'password')
    gmeet_link = st.text_input("Enter Google meet link", "")
    hr_name = st.text_input("Enter your Name", "")
    company_name = st.text_input("  Company name", "")
    c_mail = st.text_input("Enter candidate's Email","")
    
    
      
  global decision
  # main content
  job_role = st.selectbox(
     "Select the job role:",
      ['AI/ML Engineer','FrontEnd Developer','BackEnd Developer'])
    
  if job_role == 'AI/ML Engineer':
    skill = skills[0]
    st.write(skills[0])
  elif job_role == 'FrontEnd Developer':
    skill = skills[1]
    st.write(skills[1])
  else:
    skill = skills[2]
    st.write(skills[2])
    
  uploaded_file = st.file_uploader("Upload the Resume:", type=["pdf"])
  if st.button('Analyze'):
    if uploaded_file is not None:
      content = document_loader(uploaded_file)
      summary = summarizer(content)
      name = name_from_resume(content=content)
      st.write(summary)
      decision = fit_or_not(content=content,skill=skill,job_role=job_role)
       
      if decision == 'Yes':
        st.success('Congratulations, This candidate is Shortlisted.')
        with st.spinner("Sending the mail to the Candidate..."):
          status = success_email(name=name,job_role=job_role,company_name=company_name,gmeet_link=gmeet_link,content=content,sender_email=email,reciever_email=c_mail,sender_name=hr_name,password=password)
          if status == 'Success':
            st.success('Email sent to the Candidate successfully.')
          else:
            st.success("Due to some error, Email sending is not successful.")
      if decision == 'No':
        st.success('Unfortunately, This candidate is not Shortlisted.')
        with st.spinner("Sending the mail to the Candidate..."):
          status = apology_email(job_role=job_role,company_name=company_name,sender_email=email,reciever_email=c_mail,sender_name=hr_name,password=password,name=name)
          if status == 'Success':
            st.success('Email sent to the Candidate successfully.')
          else:
            st.success("Due to some error, Email sending is not successful.")

          
if __name__ == "__main__":
  main()