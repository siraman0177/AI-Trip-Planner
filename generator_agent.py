from typing import Dict, Any
from .optimizer_agent import OptimizerAgent

# ✅ use the new, non-deprecated LangChain import
try:
    from langchain_community.chat_models import ChatOpenAI
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False


class GeneratorAgent:
    """
    Generator Agent for AI Trip Planner
    -----------------------------------
    Converts optimized plan JSON into a human-readable itinerary.
    Optionally enhances output using an LLM (like GPT via LangChain).
    """

    def __init__(self, use_llm: bool = False, openai_api_key: str = None):
        self.use_llm = use_llm and LANGCHAIN_AVAILABLE
        self.openai_api_key = openai_api_key

        if self.use_llm:
            # Setup LangChain LLM (e.g., GPT-4 or GPT-3.5)
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.7,
                openai_api_key=openai_api_key
            )
            self.template = PromptTemplate(
                input_variables=["plan"],
                template=(
                    "You are a professional travel planner. "
                    "Given the following optimized itinerary JSON, "
                    "write a detailed, friendly itinerary:\n\n"
                    "{plan}\n\n"
                    "Each day should include:\n"
                    "1. An intro sentence.\n"
                    "2. Description for each place (2–3 lines).\n"
                    "3. A summary tip for the day.\n\n"
                    "Format clearly using Markdown."
                ),
            )
            self.chain = LLMChain(llm=self.llm, prompt=self.template)

    # ------------------------------------------------------------

    def generate_itinerary(self, optimized_output: Dict[str, Any]) -> Dict[str, Any]:
        """Convert optimized itinerary into readable text."""
        optimized_plan = optimized_output.get("optimized_plan", [])
        final_text = ""

        # Fallback if plan is empty
        if not optimized_plan:
            return {
                "text": "No itinerary found. Please provide valid optimized data.",
                "summary": None,
            }

        # --- Option 1: Without LLM (plain text)
        if not self.use_llm:
            lines = ["🧭 **Your Optimized Travel Itinerary**\n"]
            for day_plan in optimized_plan:
                lines.append(f"### Day {day_plan['day']}")
                lines.append(f"**Places to Visit:** {', '.join(day_plan['places'])}")
                lines.append(f"⏱️ Total Time: {day_plan['total_time']} hrs")
                lines.append(f"💰 Total Cost: ₹{day_plan['total_cost']}")
                lines.append("---")
            final_text = "\n".join(lines)
            summary = "Optimized itinerary successfully generated (text-based)."

        # --- Option 2: With LLM (narrative)
        else:
            plan_text = str(optimized_output)
            final_text = self.chain.run(plan=plan_text)
            summary = "Detailed itinerary generated using LLM."

        return {
            "text": final_text,
            "score": optimized_output.get("score", 0),
            "summary": summary,
        }

    # ------------------------------------------------------------

    def run_pipeline(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """(Optional) Run Optimizer + Generator together."""
        optimizer = OptimizerAgent()
        optimized = optimizer.optimize_itinerary(user_input)
        return self.generate_itinerary(optimized)
