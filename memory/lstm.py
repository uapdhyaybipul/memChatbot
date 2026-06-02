from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.store.memory import InMemoryStore
from langgraph.store.base import BaseStore
import os
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

store = InMemoryStore()

user_id = "u1"

user_details = ("user", user_id, "details")


store.put(user_details, "profile_1", {"data": "Name: Bipul"})
store.put(user_details, "profile_2", {"data": "Profession: learning AI on stuffs"})
store.put(user_details, "preference_1", {"data": "Prefers concise answers"})
store.put(user_details, "preference_2", {"data": "Likes examples in Python"})
store.put(user_details, "project_1", {"data": "Building MCP servers (Python-based project)"})


# ----------------------------
# 2) System prompt template (your prompt)
# ----------------------------
SYSTEM_PROMPT_TEMPLATE = """You are a helpful assistant with memory capabilities.
If user-specific memory is available, use it to personalize 
your responses based on what you know about the user.

Your goal is to provide relevant, friendly, and tailored 
assistance that reflects the user’s preferences, context, and past interactions.

If the user’s name or relevant personal context is available, always personalize your responses by:
    – Always Address the user by name (e.g., "Sure, {Name}...") when  appropriate
    – Referencing known projects, tools, or preferences (e.g., "your MCP  server python based project")
    – Adjusting the tone to feel friendly, natural, and directly aimed at the user

Avoid generic phrasing when personalization is possible. For example, instead of "In TypeScript apps..." 
say "Since your project is built with TypeScript..."

Use personalization especially in:
    – Greetings and transitions
    – Help or guidance tailored to tools and frameworks the user uses
    – Follow-up messages that continue from past context

Always ensure that personalization is based only on known user details and not assumed.

In the end suggest 3 relevant further questions based on the current response and user profile

The user’s memory (which may be empty) is provided as: {user_details_content}
"""


# ----------------------------
# 3) Create the LLM and Graph

llm = ChatGroq(model=os.getenv("CHAT_MODEL"), api_key=api_key)

def chat_node(state:MessagesState, config:RunnableConfig, store:BaseStore):
   
   user_id = config["configurable"]["user_id"]

   #Read only: fetch user details from the store(memory ,no writes)
   user_details = ("user",user_id,"details")
   print("User details tuples:", user_details)

   items= store.search(user_details)
   print("User details fetched from store:", store.search(user_details))

   if items:
      user_details_content = "\n".join([f"{item['key']}: {item['value']['data']}" for item in items])
   else:
      user_details_content = "No user details available."

   system_message = SystemMessage(content=SYSTEM_PROMPT_TEMPLATE.format(user_details_content=user_details_content,name="Bipul"))
   print("System message content:", system_message.content)

