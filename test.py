# from app.config import settings

# print("Groq API Key:", settings.groq_api_key)
# print("vision_model:", settings.vision_model)
# print("tavily_api_key:", settings.tavily_api_key)

from app.agent import graph 


config = {"configurable": {"thread_id": "user_123"}}

result = graph.invoke(
    {
        "question": "What causes headaches?",
        "history": [],
        "image_description": "",
        "kb": [],
        "web": [],
        "answer": "",
        "route": ""
    },
    config=config
)

print("Final Result:", result)