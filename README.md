#  AI Trip Planner (Multi-Agent System)

##  Overview

AI Trip Planner is a **multi-agent system** that automatically generates optimized travel itineraries based on user preferences such as destination, budget, interests, and number of travelers.

The system uses a modular pipeline consisting of:

* Research Agent (data collection & filtering)
* Optimizer Agent (scoring & selection)
* Generator Agent (final itinerary creation)

---

##  How It Works

The pipeline follows 3 main steps:

1️⃣ **Research Agent**

* Fetches and filters data (flights, hotels, activities)
* Applies scoring based on ratings, cost, and preferences

2️⃣ **Optimizer Agent**

* Selects best activities using weighted scoring
* Distributes activities across days
* Ensures budget and time optimization

3️⃣ **Generator Agent**

* Converts structured data into a readable itinerary
* Optional LLM-based enhancement using OpenAI

---

## 🛠️ Tech Stack

* Python
* Pandas
* JSON (data storage)
* LangChain (optional LLM integration)
* OpenAI API (optional)

---

##  Project Structure

```bash
ai-trip-planner/
│
├── agents/
│   ├── __init__.py
│   ├── research_agent.py
│   ├── optimizer_agent.py
│   └── generator_agent.py
│
├── tripPipeline.py        # Main pipeline logic
├── helper.py              # Test script
│
├── data/
│   ├── activities.json
│   ├── flights.json
│   └── hotels.json
│
├── requirements.txt
└── README.md
```

---

