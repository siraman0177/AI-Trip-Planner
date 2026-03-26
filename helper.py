from tripPipeline import plan_trip_pipeline  
import pandas as pd
from pprint import pprint

user_input = {
    "origin": "Mumbai",
    "destination": "Goa",
    "budget": 35000,
    "travelers": 5,
    "interests": ["beach", "food"]
}

results = (plan_trip_pipeline(user_input, use_llm=False))
# print(results['final_itinerary'])
# pprint(results)
print("\n🧭 Final Itinerary:")
print(results["final_itinerary"]["text"])

# print("\n📊 Optimization Score:", results["optimized_results"]["score"])
# print("\n🎯 Summary:", results["final_itinerary"]["summary"])

