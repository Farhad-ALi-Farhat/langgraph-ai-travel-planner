# 🌍 AI Travel Planner

An AI-powered travel planning assistant built with **LangGraph**, **LangChain**, **Groq LLM**, **Tavily Search**, and **Streamlit**.

The application analyzes a user's travel preferences, researches destinations and travel costs, selects the most suitable destination, and generates a personalized travel itinerary.

---

## ✨ Features

- 📍 AI-powered destination recommendations
- 💰 Estimated travel cost analysis
- 🚌 Transportation recommendations
- 🌦️ Weather information
- 🗓️ Day-wise itinerary generation
- 📊 Budget breakdown
- 🔍 Live travel information using Tavily Search
- ⚙️ Multi-step workflow powered by LangGraph

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangGraph
- LangChain
- Groq (Llama 3.3 70B)
- Tavily Search API
- OpenWeather API

---

## 📁 Project Structure

```text
AI-Travel-Planner/
│
├── app.py
├── graph.py
├── config.py
├── requirements.txt
├── .env.example
│
├── models/
│   └── state.py
│
├── nodes/
│   ├── extractor.py
│   ├── planner.py
│   ├── retrieval.py
│   ├── context.py
│   ├── selector.py
│   ├── decision.py
│   └── itinerary.py
│
├── tools/
│   ├── search.py
│   ├── costs.py
│   ├── weather.py
│   └── __init__.py
│
└── utils/
    └── json_utils.py
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/<your-username>/AI-Travel-Planner.git
cd AI-Travel-Planner
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

### Run the application

```bash
streamlit run app.py
```

---

## 🔄 Workflow

```
User Query
      │
      ▼
Extract User Information
      │
      ▼
Plan Required Retrievals
      │
      ▼
Retrieve Destination Information
      │
      ▼
Extract Candidate Destinations
      │
      ▼
Retrieve Destination Costs
      │
      ▼
Extract Structured Cost Information
      │
      ▼
Merge Destination & Cost Data
      │
      ▼
Select Best Destination
      │
      ▼
Generate Final Decision
      │
      ▼
Generate Day-wise Itinerary
```

---

## 💬 Example Prompt

```text
Suggest a 4-day mountain trip under PKR 100,000.
```

The planner generates:

- 📍 Recommended destination
- 💰 Estimated trip cost
- 🚌 Transport recommendation
- 🤖 Reasoning behind the recommendation
- 🗓️ Day-wise itinerary
- 💵 Budget breakdown
- ✈️ Travel tips

---

## 🚀 Future Improvements

- Hotel recommendations
- Restaurant suggestions
- Google Maps integration
- Flight and bus booking APIs
- Multi-city trip planning
- Conversation memory
- Interactive itinerary editing
- PDF itinerary export

---

## 📄 License

This project is intended for educational and portfolio purposes.