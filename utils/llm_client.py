"""LangChain Google GenAI client for KisanMitra — using langchain-google-genai and LCEL."""
import os
import json
import re
from typing import Optional, Any
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()


class GeminiClient:
    """LangChain Google GenAI wrapper with automatic model fallbacks and robust JSON parsing."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        self.api_key = api_key

        # Fallback chain across resilient flash models
        self.primary_llm = ChatGoogleGenerativeAI(
            model="gemini-flash-lite-latest",
            google_api_key=self.api_key,
            temperature=0.2,
            max_retries=3,
        )

        self.fallback_llm1 = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=self.api_key,
            temperature=0.2,
            max_retries=3,
        )

        self.fallback_llm2 = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            google_api_key=self.api_key,
            temperature=0.2,
            max_retries=3,
        )

        self.llm = self.primary_llm.with_fallbacks([self.fallback_llm1, self.fallback_llm2])
        self.json_parser = JsonOutputParser()

    def _extract_text(self, content: Any) -> str:
        """Safely extract text string from LangChain message content."""
        if isinstance(content, str):
            return content
        elif isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict):
                    parts.append(item.get("text", ""))
                else:
                    parts.append(str(item))
            return "".join(parts)
        return str(content)

    def generate(self, prompt: str, temperature: float = 0.3) -> str:
        """Generate response using LangChain."""
        try:
            res = self.llm.invoke([HumanMessage(content=prompt)])
            return self._extract_text(res.content)
        except Exception as e:
            print(f"LangChain generate error: {e}")
            return ""

    def generate_json(self, prompt: str, temperature: float = 0.1) -> Optional[list | dict]:
        """Generate and parse structured JSON using LangChain."""
        # Try direct LCEL chain with parser
        try:
            chain = self.llm | self.json_parser
            parsed = chain.invoke([HumanMessage(content=prompt)])
            if isinstance(parsed, (list, dict)):
                return parsed
        except Exception:
            pass

        # Fallback manual extraction and regex cleaning
        raw = self.generate(prompt, temperature=temperature)
        if not raw:
            return None

        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)
            cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            json_match = re.search(r'(\[.*\]|\{.*\})', cleaned, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass
            print(f"Failed to parse JSON from LangChain output: {raw[:200]}")
            return None
