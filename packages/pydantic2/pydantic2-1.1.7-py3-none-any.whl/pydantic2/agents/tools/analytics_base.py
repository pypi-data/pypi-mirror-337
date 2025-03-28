from typing import Dict, Any
from abc import ABC
import json
from ..providers.base import ProviderBase


class BaseAnalyticsTools(ABC):
    """
    Base class for analytics tools.
    These tools should only be used when form completion is 100%.
    """

    def __init__(self, provider: ProviderBase, verbose: bool = False):
        """
        Initialize analytics tools.

        Args:
            provider: LLM provider
            verbose: Enable verbose logging
        """
        self.provider = provider
        self.verbose = verbose

    async def analyze_form(
        self,
        form_data: Dict[str, Any],
        form_schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze form data and generate analysis.

        Args:
            form_data: Completed form data
            form_schema: Form JSON schema

        Returns:
            Analysis results
        """
        # Create system prompt directly
        system_prompt = f"""
        Analyze this form data and generate a comprehensive assessment.

        FORM DATA:
        ```json
        {json.dumps(form_data, indent=2)}
        ```

        FORM SCHEMA:
        ```json
        {json.dumps(form_schema, indent=2)}
        ```

        Provide a detailed analysis with relevant metrics and observations.
        Return your analysis as a structured JSON object.
        """

        try:
            # Call LLM provider with response format as JSON
            result = await self.provider.invoke(
                system=system_prompt,
                user="",
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            # Extract content from response
            content = result.choices[0].message.content

            # Convert to dictionary if it's a string
            if isinstance(content, str):
                try:
                    return json.loads(content)
                except json.JSONDecodeError as e:
                    if self.verbose:
                        print(f"JSON decode error in analysis: {e}")
                    return self.get_default_analysis_result(form_data, str(e))

            return content
        except Exception as e:
            if self.verbose:
                print(f"Analysis error: {e}")
            return self.get_default_analysis_result(form_data, str(e))

    def get_default_analysis_result(self, form_data: Dict[str, Any], error_message: str) -> Dict[str, Any]:
        """
        Get default analysis result for error handling.
        Override this method in child classes for domain-specific defaults.

        Args:
            form_data: Form data
            error_message: Error message

        Returns:
            Default analysis result
        """
        return {
            "error": error_message,
            "status": "error",
            "message": "Unable to analyze the form data"
        }
