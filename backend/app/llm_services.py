from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from dotenv import load_dotenv
from typing import List
import os

load_dotenv()

class LLMService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            temperature=0.7,
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.parser_json = JsonOutputParser()
        self.parser_str = StrOutputParser()

    def extract_keywords(self, text: str) -> List[str]:
        prompt = PromptTemplate(
            template=(
               "You are an HR and tech recruitment writing assistant.\n"
                "TASK: Extract all the most important keywords from the given text from a recruiter's perspective.\n"
                "RULES:\n"
                "1. Return only the exact keywords — do not rephrase or summarize.\n"
                "2. Each keyword must be 1–4 words long.\n"
                "3. Do not repeat keywords.\n"
                "4. Output must be a Python list of strings. No explanations, no extra text.\n"
                "4. Do not miss any keyword\n"
                "EXAMPLE OUTPUT:\n"
                '["keyword1", "keyword2", "keyword3"]\n'
                "TEXT:\n{text}\n\n"
                "OUTPUT:"
            ),
            input_variables=["text"]
        )
        chain = prompt | self.llm | self.parser_json
        return chain.invoke({"text": text})
    
    def extract_keywords_for_job(self, job_title: str) -> list[str]:
        prompt = PromptTemplate(
        template = (
            "You are an expert HR recruiter.\n"
            "TASK: For the job title: {job_title}, identify the **top 50 most important skills, technologies, qualifications, degrees, specializations, and educational institutions** "
            "that a candidate should have to be competitive for this role.\n"
            "RULES:\n"
                "1. Include skills, tools, certifications, degrees, relevant branches/specializations, and top colleges/universities (especially well-known Indian institutions like IIT only).\n"
                "2. Each keyword must be 1–4 words long.\n"
                "3. No duplicates.\n"
                "4. Output must be a valid JSON array of exactly 50 strings. No explanations, no extra text.\n"
                "5. Rank keywords based on their relevance and importance from a recruiter’s perspective.\n"
            "EXAMPLE OUTPUT:\n"
            '["Indian Institute of Technology", "Computer Science", "B.Tech", "AWS Certified Solutions Architect", "Data Structures", ... up to 50]\n'
            "OUTPUT:"
        ),
        input_variables=["job_title"]
    )

        chain = prompt | self.llm | self.parser_json
        return chain.invoke({"job_title": job_title})


    def generate_job_description(self, job_title: str) -> str:
        prompt = PromptTemplate(
            template=(
                "You are an HR and recruitment writing assistant.\n"
                "TASK: Create a detailed, professional job description for the position: {job_title}.\n"
                "REQUIREMENTS:\n"
                    "1. Include these sections in this exact order:\n"
                        "   - Job Overview\n"
                        "   - Key Responsibilities\n"
                        "   - Required Skills, Knowledge, and Experience\n"
                        "   - Preferred Qualifications\n"
                        "   - should contains program pursued like B-tech, M-tech ..."
                    "2. In 'Required Skills, Knowledge, and Experience':\n"
                        "   - List essential technical and soft skills.\n"
                        "   - Include key areas of knowledge relevant to the role.\n"
                    "3. Keep language clear, formal, and free of fluff.\n"
                    "4. Each bullet point should be concise, specific, and impactful.\n"
                    "5. Do not add any section outside of the four above.\n"
                    "6. Avoid generic placeholders — provide concrete, role-specific details.\n"
                    "7. It should be in 1-2 paragraph only"
                    "OUTPUT:"
        ),
            input_variables=["job_title"]
        )          

        chain = prompt | self.llm | self.parser_str
        return chain.invoke({"job_title": job_title})

    def generate_suggestions(self, resume_summary: str, job_desc: str, matching_issues: list[str]) -> dict:
        prompt = PromptTemplate(
        template=(
            "You are a professional resume optimization coach.\n"
            "TASK: Based on the resume summary, job description, and matching issues, "
            "provide actionable suggestions in two categories:\n"
            "1. Strengths — what the candidate does well.\n"
            "2. Areas of Improvement — specific things to improve for better job fit.\n"
            "RULES:\n"
            "1. Provide 2–4 concise suggestions for each category.\n"
            "2. Each suggestion must be 10–15 words max.\n"
            "3. Do not repeat suggestions in different words.\n"
            "4. Output strictly as a JSON object with keys 'strengths' and 'areas_of_improvement', each mapping to a list of strings.\n"
            "EXAMPLE OUTPUT:\n"
            '{{\n'
            '  "strengths": [\n'
            '    "Strong keyword match with job description",\n'
            '    "Clear presentation of technical skills"\n'
            '  ],\n'
            '  "areas_of_improvement": [\n'
            '    "Add more relevant keywords from job description",\n'
            '    "Highlight quantifiable achievements more clearly"\n'
            '  ]\n'
            '}}\n'
            "RESUME SUMMARY:\n{resume_summary}\n\n"
            "JOB DESCRIPTION:\n{job_desc}\n\n"
            "MATCHING ISSUES:\n{matching_issues}\n\n"
            "OUTPUT:"
        ),
        input_variables=["resume_summary", "job_desc", "matching_issues"]
    )
        chain = prompt | self.llm | self.parser_json
        return chain.invoke({
            "resume_summary": resume_summary,
            "job_desc": job_desc,
            "matching_issues": ", ".join(matching_issues)
        })



    def generate_cover_letter(self, resume_summary: str, job_title: str, job_desc: str,
                          recipient_name: str, recipient_title: str, recipient_company: str,
                          recipient_location: str, recipient_email: str) -> dict:
        prompt = PromptTemplate(
        template=(
            "You are an expert professional cover letter writer.\n"
            "TASK: Generate a detailed cover letter JSON for a candidate applying to the role: {job_title}.\n"
            "REQUIREMENTS:\n"
            "1. Use the following recipient details:\n"
            "   - Name: {recipient_name}\n"
            "   - Title: {recipient_title}\n"
            "   - Company: {recipient_company}\n"
            "   - Location: {recipient_location}\n"
            "   - Email: {recipient_email}\n"
            "2. Extract or generate candidate info: full_name, email, phone, location, linkedin, twitter if exist.\n"
            "3. Include candidate's college, key skills (list), and projects (list if exist).\n"
            "4. Write the full cover letter body as a single string under 'body', starting with a greeting addressing the recipient by name.\n"
            "5. Keep cover letter concise, professional, and tailored to the job description and resume summary.\n"
            "6. Output must be valid JSON with the exact keys as shown below, no extra text.\n"
            "7. Do not give any details that is not in resume_summary and give only legit information.\n"
            "EXAMPLE OUTPUT:\n"
            '{{\n'
            '  \"full_name\": \"Abhinav Kumar\",\n'
            '  \"job_title\": \"Business Analyst\",\n'
            '  \"email\": \"gordon@novoresume.com\",\n'
            '  \"phone\": \"000 123 4455\",\n'
            '  \"location\": \"Lyon, France\",\n'
            '  \"linkedin\": \"linkedin.com/in/gordan.shandiin\",\n'
            '  \"twitter\": \"@gordan.shandiin\",\n'
            '  \"recipient_name\": \"Maria Smith\",\n'
            '  \"recipient_title\": \"Hiring Manager\",\n'
            '  \"recipient_company\": \"BlackHills Business LLC\",\n'
            '  \"recipient_location\": \"London, UK\",\n'
            '  \"recipient_email\": \"maria@blackhills.com\",\n'
            '  \"body\": \"Dear Maria, I am writing to express my interest in the Business Analyst position... Sincerely, Gordon Shandiin\",\n'
            '  \"college\": \"IIT ISM DHANBAD\",\n'
            '  \"skills\": [\"html\", \"css\", \"js\", \"react\", \"node js\", \"express\", \"mongoDB\", \"ML\", \"DSA\"],\n'
            '  \"projects\": [\"leetcode clone\", \"swiggy clone\", \"code debugger\"]\n'
            '}}\n'
            "JOB DESCRIPTION:\n{job_desc}\n\n"
            "RESUME SUMMARY:\n{resume_summary}\n\n"
            "OUTPUT:"
        ),
        input_variables=["resume_summary", "job_title", "job_desc",
                         "recipient_name", "recipient_title", "recipient_company",
                         "recipient_location", "recipient_email"]
    )
        chain = prompt | self.llm | self.parser_json
        return chain.invoke({
        "resume_summary": resume_summary,
        "job_title": job_title,
        "job_desc": job_desc,
        "recipient_name": recipient_name,
        "recipient_title": recipient_title,
        "recipient_company": recipient_company,
        "recipient_location": recipient_location,
        "recipient_email": recipient_email
        })
