#!/usr/bin/env python
"""
Minimal example showing how to create custom analytics with BaseAnalyticsTools.
"""

import os
import asyncio
from typing import Dict, Any
import json

# Import from our library
from pydantic2.agents import BaseAnalyticsTools, OpenRouterProvider


# Create a minimal analytics class by only overriding the prompt methods
class MinimalAnalytics(BaseAnalyticsTools):
    """
    Minimal analytics implementation that only customizes the prompts.
    This demonstrates how easy it is to create a new analytics tool.
    """

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
                    print("Could not parse JSON response")
                    pass

            if isinstance(content, dict):
                return content

            # Fallback to form data itself
            return form_data

        except Exception as e:
            print(f"Analysis error: {e}")
            return form_data

    def _create_prompt(self, form_data: Dict[str, Any]) -> str:
        """
        Create analytics prompt for user profile data.

        Args:
            form_data: Form data to analyze

        Returns:
            Prompt string for analysis
        """
        return f"""
        You are a data analyst specializing in user profile data.
        Analyze this user profile and provide insights.

        USER DATA:
        ```json
        {json.dumps(form_data, indent=2)}
        ```

        Produce a brief analysis with these components:
        1. User demographic category (student, professional, retired, etc.)
        2. Main interests or skills
        3. Career stage assessment

        Return your analysis as a simple JSON object with these three fields.
        """


async def demo():
    """Run a demo of the minimal analytics."""
    api_key = os.environ.get("OPENROUTER_API_KEY", "dummy_key_for_demo")

    # Sample user data
    user_data = {
        "name": "Alex Chen",
        "age": 28,
        "occupation": "Software Developer",
        "skills": ["Python", "JavaScript", "Machine Learning"],
        "education": "Bachelor's in Computer Science",
        "goals": "Transition to a machine learning engineer role"
    }

    # Create provider
    provider = OpenRouterProvider(api_key=api_key)

    print("MINIMAL ANALYTICS DEMO")
    print("=" * 50)

    print("\nRunning analysis...")
    analytics_instance = MinimalAnalytics(provider=provider, verbose=True)
    analysis = analytics_instance.analyze(user_data)
    print(f"Analysis result:\n{json.dumps(analysis, indent=2)}")

    print("\nDemo complete! Notice how we only needed to define the _create_prompt method.")


if __name__ == "__main__":
    asyncio.run(demo())
