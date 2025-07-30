from phi.agent import Agent
from phi.model.google import Gemini
import os
from dotenv import load_dotenv

load_dotenv(override=True)

google_api_key = os.getenv("GEMINI_API_KEY")

llm = Agent(
    model=Gemini(id="gemini-2.0-flash", api_key=google_api_key),
    markdown=True,
)
