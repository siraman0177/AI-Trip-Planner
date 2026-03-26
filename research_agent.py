import geocoder
import requests
import pandas as pd
from datetime import datetime, timedelta
import json
def detect_origin():
    g = geocoder.ip('me')
    return g.city if g.city else "Delhi"

def detect_travel_dates():
    start = datetime.now() + timedelta(days=7)
    end = start + timedelta(days=3)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

def detect_season_from_date(start_date):
    m = int(start_date.split("-")[1])
    if 3 <= m <= 5: return "summer"
    elif 6 <= m <= 9: return "monsoon"
    elif 10 <= m <= 11: return "autumn"
    else: return "winter"

def detect_food_preference(destination):
    pref = {"Goa":"seafood","Rishikesh":"veg","Kerala":"seafood","Jaipur":"veg"}
    return pref.get(destination,"mixed")

def detect_region_type(destination):
    region = {"Goa":"beach","Manali":"mountain","Jaipur":"urban","Kerala":"forest"}
    return region.get(destination,"urban")

def weighted_research_scoring(data_list, category, weights):
    result = []
    for item in data_list:
        try:
            if category == "hotel":
                r = float(item.get("rating", 0))
                p = float(item.get("price", 0))
                d = float(item.get("distance", 0))
                score = (r*weights["rating"]) + ((1/(p+1))*100*weights["price"]) - (d*weights["distance"])
            elif category == "flight":
                p = float(item.get("price", 0))
                dur = float(item.get("duration_hours", 1))
                ar = float(item.get("airline_rating", 3))
                score = ((1/(p+1))*100*weights["price"]) + ((1/(dur+1))*50*weights["duration"]) + (ar*weights["airline_rating"])
            elif category == "activity":
                r = float(item.get("rating", 0))
                c = float(item.get("price", 0))
                rev = float(item.get("reviews", 1000))
                score = (r*weights["rating"]) + (min(rev/3000,1)*5*weights["popularity"]) - (c*0.001)
            item["score"] = round(score, 2)
            result.append(item)
        except Exception as e:
            print("Error scoring item:", e, item)
    return sorted(result, key=lambda x: x["score"], reverse=True)

WEIGHTS = {
    "hotel": {"rating":0.5,"price":0.3,"distance":0.2},
    "flight":{"price":0.5,"duration":0.3,"airline_rating":0.2},
    "activity":{"rating":0.5,"popularity":0.3,"cost":0.2}
}

def load_local_data(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return []
    

flights_data = load_local_data(r"D:\coding\ai trip planner\data\flights.json")
hotels_data = load_local_data(r"D:\coding\ai trip planner\data\hotels.json")
activities_data = load_local_data(r"D:\coding\ai trip planner\data\activities.json")

# print(f"Flights: {len(flights_data)} | Hotels: {len(hotels_data)} | Activities: {len(activities_data)}")

def research_agent(user_input):
    destination = user_input.get("destination", "Goa").title()
    budget = user_input.get("budget", 30000)
    interests = user_input.get("interests", ["beach"])
    travelers = user_input.get("travelers", 1)
    origin = user_input.get("origin") or detect_origin()  # detect automatically if not given
    start, end = detect_travel_dates()
    season = detect_season_from_date(start)
    food_pref = detect_food_preference(destination)
    region_type = detect_region_type(destination)

    print(f"Researching {destination} trip for {travelers} traveler(s) from {origin} — Season: {season} | Food: {food_pref}")

    # Normalize text
    def normalize(t): return str(t).strip().lower()

    dest_lower = normalize(destination)
    origin_lower = normalize(origin)

    # ---------- Filter Data ----------
    hotels = [h for h in hotels_data if normalize(h.get("destination")) == dest_lower]

    # ✅ NEW: Only flights from user’s origin TO destination
    flights = [
        f for f in flights_data
        if normalize(f.get("to")) == dest_lower and normalize(f.get("from")) == origin_lower
    ]

    activities = [a for a in activities_data if normalize(a.get("destination")) == dest_lower]

    if not hotels:
        print(f"⚠️ No hotels found for {destination}")
    if not flights:
        print(f"⚠️ No flights found from {origin} to {destination}")
    if not activities:
        print(f"⚠️ No activities found for {destination}")

    # ---------- Score and rank ----------
    if hotels: hotels = weighted_research_scoring(hotels, "hotel", WEIGHTS["hotel"])
    if flights: flights = weighted_research_scoring(flights, "flight", WEIGHTS["flight"])
    if activities: activities = weighted_research_scoring(activities, "activity", WEIGHTS["activity"])

    # ---------- Print summaries ----------
    # if hotels:
    #     print(f"\n🏨 Top 5 Hotels in {destination}:")
    #     print(pd.DataFrame(hotels).head(5)[["name","price","rating","distance","score"]])

    # if flights:
    #     print(f"\n✈️ Flights from {origin} → {destination}:")
    #     print(pd.DataFrame(flights).head(5)[["airline","from","to","price","duration_hours","score"]])

    # if activities:
    #     print(f"\n🎯 Top 5 Activities in {destination}:")
    #     print(pd.DataFrame(activities).head(5)[["name","type","rating","reviews","score"]])

    return {
        "origin": origin,
        "destination": destination,
        "budget": budget,
        "season": season,
        "region_type": region_type,
        "food_preference": food_pref,
        "travelers": travelers,
        "interests": interests,
        "flights": flights[:10],
        "hotels": hotels[:10],
        "activities": activities[:15]
    }

# user_query = {
#     "origin":"mumbai",
#     "destination":"Goa",
#     "budget":30000,
#     "interests":["beach","food"]
# }

# results = researchAgent(user_query)
# # pd.DataFrame(results).head()
# pd.DataFrame(results["flights"]).head()
