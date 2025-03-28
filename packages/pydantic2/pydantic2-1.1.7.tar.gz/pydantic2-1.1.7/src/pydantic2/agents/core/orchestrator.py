from typing import Dict, Any, List, Optional, Type
from pydantic import BaseModel

from ..models.dependencies import FormDependencies
from ..models.results import FormResult
from ..models.state import FormState
from ..tools.form_tools import FormTools
from ..tools.analytics_base import BaseAnalyticsTools
from ..utils.text_sanitizer import sanitize_text


class Orchestrator:
    """
    Orchestrator for form processing.
    Manages the coordination between form tools and analytics tools.
    """

    def __init__(
        self,
        form_tools: FormTools,
        analytics_tools: Optional[BaseAnalyticsTools] = None,
        verbose: bool = False
    ):
        """
        Initialize orchestrator.

        Args:
            form_tools: Form tools for data extraction and question generation
            analytics_tools: Analytics tools for form analysis (optional)
            verbose: Enable verbose logging
        """
        self.form_tools = form_tools
        self.analytics_tools = analytics_tools
        self.verbose = verbose

    async def process(
        self,
        message: str,
        form_state: FormState,
        form_class: Type[BaseModel],
        session_id: str,
        user_id: str,
        message_history: List[Dict[str, Any]]
    ) -> FormResult:
        """
        Process a user message.

        Args:
            message: User message
            form_state: Current form state
            form_class: Form class
            session_id: Session ID
            user_id: User ID
            message_history: Message history

        Returns:
            Processing result
        """
        # Sanitize user message to protect against HTML/JavaScript injection
        sanitized_message = sanitize_text(message) if message else ""

        # Get form data - handle both dict and Pydantic model cases
        form_data = {}
        if isinstance(form_state.form, dict):
            form_data = form_state.form
        elif isinstance(form_state.form, BaseModel):
            # Use model_dump or dict method based on Pydantic version
            if hasattr(form_state.form, "model_dump"):
                form_data = form_state.form.model_dump()
            else:
                form_data = form_state.form.dict()

        # Prepare dependencies
        deps = FormDependencies(
            form_class=form_class,
            form_data=form_data,
            user_id=user_id,
            session_id=session_id,
            progress=form_state.settings.progress,
            message_history=message_history,
            user_language=form_state.settings.language,
            verbose=self.verbose
        )

        # Detect user language
        user_language = form_state.settings.language
        if sanitized_message:
            try:
                user_language = await self.form_tools.detect_user_language(sanitized_message)
            except Exception as e:
                if self.verbose:
                    print(f"Language detection error: {e}")

        # Process with analytics tools if form is complete and analytics tools exist
        if form_state.is_complete() and self.analytics_tools:
            # Process with analytics tools
            return await self._process_with_analytics(sanitized_message, deps, user_language)
        else:
            # Process with form tools
            return await self._process_with_form_tools(sanitized_message, deps, user_language)

    async def _process_with_form_tools(
        self,
        message: str,
        deps: FormDependencies,
        user_language: str
    ) -> FormResult:
        """
        Process message with form tools.

        Args:
            message: User message (sanitized)
            deps: Form dependencies
            user_language: User language

        Returns:
            Form processing result
        """
        # Extract data from message
        if message:
            updated_data = await self.form_tools.extract_data_from_message(
                message=message,
                form_data=deps.form_data,
                form_class=deps.form_class
            )
        else:
            updated_data = deps.form_data.copy()

        # Calculate progress
        progress = await self.form_tools.calculate_progress(
            form_data=updated_data,
            form_class=deps.form_class
        )

        # Generate next question
        next_question = await self.form_tools.generate_next_question(
            form_data=updated_data,
            form_class=deps.form_class,
            progress=progress,
            message_history=deps.message_history,
            user_language=user_language
        )

        # Determine response message
        if progress > deps.progress:
            if user_language.lower().startswith("ru"):
                response = f"Спасибо за информацию! {next_question}"
            else:
                response = f"Thank you for the information! {next_question}"
        else:
            response = next_question

        # Check if completion was achieved
        completion_achieved = progress >= 100

        return FormResult(
            message=response,
            form_update=updated_data,
            progress=progress,
            next_question=next_question,
            user_language=user_language,
            completion_achieved=completion_achieved
        )

    async def _process_with_analytics(
        self,
        message: str,
        deps: FormDependencies,
        user_language: str
    ) -> FormResult:
        """
        Process message with analytics tools.

        Args:
            message: User message (sanitized)
            deps: Form dependencies
            user_language: User language

        Returns:
            Analytics processing result
        """
        # Get form schema
        schema = await self.form_tools.get_form_schema(deps.form_class)

        # Analyze form data
        analysis = await self.analytics_tools.analyze_form(
            form_data=deps.form_data,
            form_schema=schema
        )

        # Format response based on analysis
        if user_language.lower().startswith("ru"):
            intro = "Вот результаты анализа:\n\n"
            next_question = "Хотите узнать что-нибудь ещё?"
        else:
            intro = "Here are the analysis results:\n\n"
            next_question = "Would you like to know anything else?"

        # Format response from analysis directly
        response_parts = [intro]

        # Add conclusion if available
        if "conclusion" in analysis:
            response_parts.append(analysis["conclusion"])

        # Add highlights if available
        if "highlights" in analysis and isinstance(analysis["highlights"], list):
            highlights = "\n".join([f"• {item}" for item in analysis["highlights"]])
            response_parts.append(f"\n\n{highlights}")

        response = "\n".join(response_parts)

        return FormResult(
            message=response,
            form_update=deps.form_data,  # No update to form data
            progress=100,  # Already completed
            next_question=next_question,
            user_language=user_language,
            analytics_result=analysis,  # Store complete analysis result
            completion_achieved=True
        )
