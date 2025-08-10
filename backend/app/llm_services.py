from langchain_core.prompts import PromptTemplate
from langchain_cohere import ChatCohere
from langchain_core.output_parsers import CommaSeparatedListOutputParser,StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.llm = ChatCohere(
            temperature=0.7,
            cohere_api_key=os.getenv("COHERE_API_KEY"),
            model_name="command"
        )
        self.parser = StrOutputParser()

    def extract_keywords(self, text: str) -> list[str]:
        prompt = PromptTemplate(
            template="Extract the most important 10-15 keywords from the following text:\n{text}\nKeywords:",
            input_variables=["text"]
        )
        chain = prompt | self.llm | CommaSeparatedListOutputParser()
        return chain.invoke({"text": text})

    def generate_job_description(self, job_title: str) -> str:
        prompt = PromptTemplate(
            template="Generate a detailed job description for a {job_title} position including key responsibilities and required skills.",
            input_variables=["job_title"]
        )
        chain = prompt | self.llm | self.parser
        return chain.invoke({"job_title": job_title})

    def generate_suggestions(self, resume_summary: str, job_desc: str, matching_issues: list[str]) -> list[str]:
        prompt = PromptTemplate(
            template=(
                "Based on the resume summary and job description, provide 3-5 actionable suggestions "
                "to improve the resume.\n\nResume Summary:\n{resume_summary}\n\nJob Description:\n{job_desc}"
                "\n\nIdentified Matching Issues:\n{matching_issues}\n\nSuggestions:"
            ),
            input_variables=["resume_summary", "job_desc", "matching_issues"]
        )
        chain = prompt | self.llm | CommaSeparatedListOutputParser()
        return chain.invoke({
            "resume_summary": resume_summary,
            "job_desc": job_desc,
            "matching_issues": ", ".join(matching_issues)
        })

    def generate_cover_letter(self, resume_summary: str, job_title: str, job_desc: str) -> str:
        prompt = PromptTemplate(
            template=(
                "Write a professional cover letter for a candidate with the following resume summary "
                "applying for a {job_title} position.\n\nJob Description:\n{job_desc}"
                "\n\nResume Summary:\n{resume_summary}\n\nCover Letter:"
            ),
            input_variables=["resume_summary", "job_title", "job_desc"]
        )
        chain = prompt | self.llm | self.parser
        return chain.invoke({
            "resume_summary": resume_summary,
            "job_title": job_title,
            "job_desc": job_desc
        })
