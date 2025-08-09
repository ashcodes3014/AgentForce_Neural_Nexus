from langchain_core.prompts import PromptTemplate
from langchain_cohere import ChatCohere
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

class Filtering:
    def __init__(self):
        self.llm = ChatCohere(
            temperature=0.7,
            cohere_api_key=os.getenv("COHERE_API_KEY"),
            model_name="command"
        )

    def extract_text(self, text: str) -> str:
        output_parser = StrOutputParser()
        prompt = PromptTemplate(
            template=(
                "You are an expert resume analyst. "
                "Given the complete text of a candidate's resume below, "
                "identify the most important information such as their key skills, "
                "major achievements, professional experience, and notable qualifications. "
                "Summarize these points in a concise, well-structured paragraph "
                "that clearly highlights the person's professional profile.\n\n"
                "Resume:\n{text}\n\n"
                "Summary:"
            ),
            input_variables=["text"]
        )
        chain = prompt | self.llm | output_parser
        return chain.invoke({"text": text})

    def extract_text_from_object(self, obj: dict) -> str:
        output_parser = StrOutputParser()
        prompt = PromptTemplate(
            template=(
                "if data is empty return empty string. "
                "You are an expert resume analyst. "
                "Given the complete dict of a candidate's details below, "
                "identify the most important information such as their key skills, "
                "major achievements, professional experience, and notable qualifications. "
                "Summarize these points in a concise, well-structured paragraph "
                "that clearly highlights the person's professional profile.\n\n"
                "Resume:\n{data}\n\n"
                "Summary:"
            ),
            input_variables=["data"]
        )
        chain = prompt | self.llm | output_parser
        return chain.invoke({"data": obj})
