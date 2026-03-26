from typing import List, Dict, Any

class OptimizerAgent:
    """
    Optimizer Agent for AI Trip Planner
    -----------------------------------
    Selects the best combination of activities (and optionally hotels/flights)
    based on user preferences, ratings, and time/cost constraints.
    """

    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or {
            "rating": 0.4,         # importance of place rating
            "cost": 0.3,           # lower cost = better
            "time": 0.2,           # shorter duration = better
            "interest_bonus": 0.1   # bonus for matching user interests
        }

    # ------------------------------------------------------------

    def score_place(self, place: Dict[str, Any], preferences: Dict[str, Any]) -> float:
        """Assign a normalized score (0–1) to each activity."""
        budget = max(preferences.get("budget", 1), 1)
        rating = float(place.get("rating", 3.0)) / 5.0
        cost = place.get("price") or place.get("cost") or 0
        time_required = place.get("time_required", 2.0)
        category = place.get("type") or place.get("category")

        # Normalize cost and time
        cost_norm = 1.0 - min(cost / budget, 1.0)
        time_norm = 1.0 - min(time_required / 8.0, 1.0)

        # Bonus for interest match
        interest_bonus = 1.0 if category in preferences.get("interests", []) else 0.0

        score = (
            self.weights["rating"] * rating +
            self.weights["cost"] * cost_norm +
            self.weights["time"] * time_norm +
            self.weights["interest_bonus"] * interest_bonus
        )
        return round(score, 4)

    # ------------------------------------------------------------

    def pack_days(
        self,
        sorted_activities: List[Dict[str, Any]],
        days: int,
        daily_hours: float = 8.0
    ) -> List[Dict[str, Any]]:
        """
        Distribute activities across days until the daily time limit is reached.
        """
        itinerary, idx = [], 0
        for day in range(1, days + 1):
            time_used, day_places = 0.0, []
            while (
                idx < len(sorted_activities)
                and time_used + sorted_activities[idx].get("time_required", 2.0) <= daily_hours
            ):
                day_places.append(sorted_activities[idx])
                time_used += sorted_activities[idx].get("time_required", 2.0)
                idx += 1

            itinerary.append({
                "day": day,
                "places": [p.get("name", "Unknown") for p in day_places],
                "total_time": round(time_used, 2),
                "total_cost": round(sum(p.get("price") or p.get("cost") or 0 for p in day_places), 2)
            })

        return itinerary

    # ------------------------------------------------------------

    def optimize_itinerary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main optimization entry point.
        Compatible with ResearchAgent's output.
        """
        # Get activities (the main things to visit)
        activities = data.get("activities", [])
        if not activities:
            return {"optimized_plan": [], "score": 0.0, "error": "No activities found"}

        # Preferences
        prefs = {
            "budget": data.get("budget", 30000),
            "interests": data.get("interests", []),
            "days": data.get("days", 2),
            "daily_hours": data.get("daily_hours", 8)
        }

        # Score and sort activities
        for act in activities:
            act["score"] = self.score_place(act, prefs)

        sorted_acts = sorted(activities, key=lambda x: x["score"], reverse=True)

        # Group into days
        itinerary = self.pack_days(sorted_acts, prefs["days"], prefs["daily_hours"])

        avg_score = sum(a["score"] for a in sorted_acts) / len(sorted_acts)
        return {
            "optimized_plan": itinerary,
            "score": round(avg_score, 3)
        }
