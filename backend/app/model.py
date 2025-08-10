from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

class Filtering:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            temperature=0.7,
            model="gemini-2.5-flash"
        )
        self.output_parser = StrOutputParser()

    def extract_text(self, text: str) -> str:
        prompt = PromptTemplate(
            template=(
                "You are a professional resume analyst.\n"
                "Read the candidate details below and produce a concise summary of their most important qualifications.\n"
                "Focus on:\n"
                "• Core skills and technical expertise\n"
                "• Key achievements and measurable impact\n"
                "• Relevant industries and domains of experience\n"
                "• Notable certifications or education (only if significant)\n\n"
                "• Do not miss any information include all things properly\n"
                "Rules:\n"
                "1. Use a formal, factual tone.\n"
                "2. Avoid generic praise or unnecessary adjectives.\n"
                "3. Do not repeat trivial information (e.g., hobbies, personal details).\n"
                "4. Limit the summary to **a single paragraph under 250 words**.\n"
                "5. Output only the summary text — no JSON, no labels.\n\n"
                "6. Do not repeat things. \n\n"
                "CANDIDATE DETAILS:\n{data}"
            ),
            input_variables=["data"]
        )
        chain = prompt | self.llm | self.output_parser
        raw_output = chain.invoke({"data": text})

        return raw_output

    def extract_text_from_object(self, obj: dict) -> str:
        data_str = "\n".join(f"{k}: {v}" for k, v in obj.items() if v)

        prompt = PromptTemplate(
            template=(
                "You are a professional resume analyst.\n"
                "Read the candidate details below and produce a concise summary of their most important qualifications.\n"
                "Focus on:\n"
                "• Core skills and technical expertise\n"
                "• Key achievements and measurable impact\n"
                "• Relevant industries and domains of experience\n"
                "• Notable certifications or education (only if significant)\n\n"
                "• Do not miss any information include all things properly\n"
                "Rules:\n"
                "1. Use a formal, factual tone.\n"
                "2. Avoid generic praise or unnecessary adjectives.\n"
                "3. Do not repeat trivial information (e.g., hobbies, personal details).\n"
                "4. Limit the summary to **a single paragraph under 250 words**.\n"
                "5. Output only the summary text — no JSON, no labels.\n\n"
                "CANDIDATE DETAILS:\n{data}"
            ),
            input_variables=["data"]
        )

        chain = prompt | self.llm | self.output_parser
        return chain.invoke({"data": data_str})

    def merge_duplicates(self, text1: str, text2: str) -> str:
        prompt = PromptTemplate(
            template=(
                "You are an expert at merging text while avoiding redundancy.\n"
                "Given two pieces of content, combine them into a single coherent paragraph.\n"
                "Rules:\n"
                "1. Remove repeated or overlapping information.\n"
                "2. Preserve all unique and important details.\n"
                "3. Keep it concise and logically flowing.\n"
                "4. Do not change factual information.\n"
                "5. Output only the merged text — no explanations, no labels.\n\n"
                "6. combine both of them and do not miss any infomation"
                "TEXT 1:\n{text1}\n\n"
                "TEXT 2:\n{text2}\n\n"
                "MERGED TEXT:"
            ),
            input_variables=["text1", "text2"]
        )

        chain = prompt | self.llm | self.output_parser
        return chain.invoke({"text1": text1, "text2": text2})