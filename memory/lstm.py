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

def get_namespace(user_id: str, memory_type: str):
    return ("user", user_id, memory_type)


#user_details = namespace

#user/==>  First level - Memory category.
# └── u1/ ==> Second level - User-specific identifier (e.g., user ID).
#      └── details/ ==> Third level - Specific type of information (e.g., "details", "preferences", "projects").

#store.put(user_details , key, value)  # Example: store.put(("user", "u1", "details"), "profile_1", {"data": "Name: Bipul"})
store.put( get_namespace("u1", "profile"), "name", {"value": "Bipul"})

store.put(    get_namespace("u1", "Learning"),  "profession",  {"value": "Learning AI"})

store.put( get_namespace("u1", "preferences"), "answer_style", {"value": "Concise"})

store.put(get_namespace("u1", "preferences"), "language", {"value": "Python"})

store.put(get_namespace("u1", "projects"),    "project_1",    {"value": "Building MCP servers"})

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


def fetch_user_memory(store, user_id):

    memory_types = ["profile","preferences", "projects","goals", "facts"]

    memory = {}

    for memory_type in memory_types:

        namespace = get_namespace(user_id, memory_type)

        items = store.search(namespace)

        memory[memory_type] = {}

        for item in items:
            memory[memory_type][item.key] = item.value.get("value")

    return memory


def extract_prompt_variables(memory):

    return {
        "Name": memory.get("profile", {})
                     .get("name", "User"),

        "Profession": memory.get("profile", {})
                           .get("profession", "Unknown"),

        "AnswerStyle": memory.get("preferences", {})
                            .get("answer_style", "Normal"),

        "Language": memory.get("preferences", {})
                          .get("language", "Unknown")
    }


def build_memory_context(memory):

    lines = []

    for category, values in memory.items():

        if not values:
            continue

        lines.append(f"\n{category.upper()}:")

        for key, value in values.items():
            lines.append(f"- {key}: {value}")

    return "\n".join(lines)

def chat_node(state: MessagesState,config: RunnableConfig,store: BaseStore):

    user_id = config["configurable"]["user_id"]

    user_memory = fetch_user_memory( store, user_id)

    print("Fetched User Memory:", user_memory)

    prompt_variables = extract_prompt_variables(user_memory)

    # Build readable memory context
    memory_context = build_memory_context(user_memory)

    system_message = SystemMessage(
        content=SYSTEM_PROMPT_TEMPLATE.format(user_details_content=memory_context,Name=prompt_variables["Name"]) )
    llm = ChatGroq(api_key=api_key, model=os.getenv("CHAT_MODEL"))

    response = llm.invoke([system_message] + state["messages"])

    print(response.content)


builder = StateGraph(MessagesState)
builder.add_node("chat", chat_node)
builder.add_edge(START, "chat")
builder.add_edge("chat", END)

graph = builder.compile(store=store)

# ----------------------------
# 4) Run it (provide user_id in config)
# ----------------------------
config = {"configurable": {"user_id": "u1"}}

result = graph.invoke(
    {"messages": [{"role": "user", "content": "Explain gen ai in simple terms."}]},
    config,
)

print(result["messages"][-1].content)


# chat_node(state=None, config={"configurable": {"user_id": "u1"}}, store=store)
