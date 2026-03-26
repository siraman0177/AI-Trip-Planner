from agents import research_agent, OptimizerAgent, GeneratorAgent

# from optimizerAgent import OptimizerAgent
# from generatorAgent import GeneratorAgent

def plan_trip_pipeline(user_input: dict, use_llm: bool = False, openai_api_key: str = None) -> dict:
    """
    Master pipeline function for AI Trip Planner.
    Runs:
    1️⃣ Research Agent -> fetches and filters data
    2️⃣ Optimizer Agent -> selects best itinerary
    3️⃣ Generator Agent -> converts to human-readable text
    """

    print("🔍 Step 1: Running Research Agent...")
    research_results = research_agent(user_input)
    if not research_results:
        return {"error": "Research Agent returned no data. Check destination or dataset."}

    print("\n⚙️ Step 2: Running Optimizer Agent...")
    optimizer = OptimizerAgent()
    optimized_results = optimizer.optimize_itinerary(research_results)
    if not optimized_results or not optimized_results.get("optimized_plan"):
        return {"error": "Optimizer Agent failed to generate a valid plan."}

    print("\n🧠 Step 3: Running Generator Agent...")
    generator = GeneratorAgent(use_llm=use_llm, openai_api_key=openai_api_key)
    final_output = generator.generate_itinerary(optimized_results)

    print("\n✅ Trip planning pipeline completed successfully!")

    return {
        "input": user_input,
        "research_results": research_results,
        "optimized_results": optimized_results,
        "final_itinerary": final_output
    }
