import json
from groq import Groq


class AIComparisonService:
    """
    Handles all AI-related logic.
    Responsible ONLY for building prompts and retrieving AI responses.
    """

    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def _build_prompt(self, offers: list, priority: str) -> str:
        """
        Builds a structured prompt for the AI model.
        Keeping this separate allows easy prompt iteration later.
        """
        return f"""
    You are a telecommunications expert. I will provide you with two offer plans and a user's priority.
    Your task is to compare the two offers and determine which one is better based on the given priority.

    Rules for your comparison:
    - Be objective and clear.
    - Do not make a choice for the user. Instead, explain the pros and cons distinctively of each plan as they relate to the priority.
    - End your response with a section titled "Conclusion" on its own line, followed by a single-line summary stating which plan is the better value for the given priority, and why.
    - The output should be professional and easy to read.
    - Use "denars" as the currency for all prices.
    - DO NOT use any markdown formatting like bolding (**), headings (##), or lists (*). The formatting will be handled separately.
    - DO NOT list the offer features again, just focus on the pros and cons and conclusion.
    - Lower price is always a PRO.
    
    FYI 'Safe' is a safe of all your internet data the user hasn't used, it accumulates up to 150GB, a good feature to not waste your unused internet from previous months.
    
    Here are the two offers in JSON format: Offers: {json.dumps(offers)}
    Here is the user's priority: Priority: {priority}

    Your analysis:
    """

    def compare_offers(self, offers: list, priority: str) -> str:
        """
        Sends the comparison request to the AI model and
        returns the generated analysis text.
        """
        prompt = self._build_prompt(offers, priority)

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content
