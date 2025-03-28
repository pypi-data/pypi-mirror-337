#!/usr/bin/env python
"""
Simple form example for the Pydantic AI Form Processor.
"""

import os
import asyncio
from typing import List, Dict, Any
from pydantic import BaseModel, Field
import json

# Import from our library
from pydantic2.agents import FormProcessor
from pydantic2.agents import BaseAnalyticsTools, OpenRouterProvider

# Get API key from environment
API_KEY = os.environ.get("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("Please set the OPENROUTER_API_KEY environment variable")


# Define a simple form
class SimpleForm(BaseModel):
    name: str = Field(default="", description="User's full name")
    age: int = Field(default=0, description="User's age in years")
    occupation: str = Field(default="", description="User's current job or occupation")
    interests: List[str] = Field(default_factory=list, description="User's hobbies and interests")
    goals: str = Field(default="", description="User's professional or personal goals")


# Simple analytics implementation
class SimpleAnalytics(BaseAnalyticsTools):
    def run_async(self, coroutine):
        """Run async coroutine synchronously"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coroutine)
        finally:
            loop.close()

    def analyze(self, form_data: Dict[str, Any], session_id: str = None) -> Dict[str, Any]:
        """
        Analyze form data and return structured results.

        Args:
            form_data: Form data to analyze
            session_id: Optional session ID

        Returns:
            Analysis results as dict
        """
        try:
            # Create prompt for analysis
            prompt = self._create_prompt(form_data)

            # Call LLM provider
            result = self.run_async(self.provider.invoke(
                system=prompt,
                user="",
                temperature=0.7,
                response_format={"type": "json_object"}
            ))

            # Extract and parse content
            content = result.choices[0].message.content

            if isinstance(content, str):
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    if self.verbose:
                        print("Could not parse JSON response")
                    pass

            if isinstance(content, dict):
                return content

            # Fallback to form data itself
            return {"error": "Failed to analyze form data"}

        except Exception as e:
            if self.verbose:
                print(f"Analysis error: {e}")
            return {"error": str(e)}

    def _create_prompt(self, form_data: Dict[str, Any]) -> str:
        """
        Create analytics prompt for personal profile analysis.

        Args:
            form_data: Form data to analyze

        Returns:
            Prompt string for analysis
        """
        return f"""
        Analyze this personal profile data and generate a professional assessment.

        USER DATA:
        ```json
        {json.dumps(form_data, indent=2)}
        ```

        ASSESSMENT CRITERIA:
        1. Career stage (early, mid, senior)
        2. Growth potential
        3. Interest diversity

        Return a JSON analysis with these fields.
        """


async def main():
    # Create provider
    provider = OpenRouterProvider(
        api_key=API_KEY,
        model_name="openai/gpt-4o-mini"
    )

    # Create analytics
    analytics = SimpleAnalytics(provider=provider, verbose=True)

    # Create form processor
    processor = FormProcessor(
        form_class=SimpleForm,
        analytics_tools=analytics,
        openrouter_api_key=API_KEY,
        verbose=True
    )

    # Initialize session
    session_id, first_question = await processor.initialize()
    print(f"\nSession: {session_id}")
    print(f"Assistant: {first_question}")

    # Simulate a conversation
    messages = [
        "My name is John Smith and I'm 32 years old",
        "I work as a software engineer at a tech startup",
        "I enjoy hiking, coding, and playing chess in my free time",
        "My goal is to become a senior developer and eventually start my own company",
        "Can you analyze my profile?"
    ]

    for message in messages:
        print(f"\nUser: {message}")
        result = await processor.process_message(message, session_id)
        print(f"Assistant: {result.message}")
        print(f"Progress: {result.progress}%")

    # Get final form state
    state = await processor.get_form_state(session_id)
    print("\nFinal form data:")
    print(state.form)

if __name__ == "__main__":
    asyncio.run(main())
