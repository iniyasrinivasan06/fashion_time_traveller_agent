"""
agent.py
Builds the ReAct-style agent using native tool-calling (more reliable than
text-based ReAct parsing on smaller/free models). The Thought -> Action ->
Observation loop still happens, just via structured function calls instead
of raw text parsing.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tools import scrape_fashion_history, cycle_pattern_analyzer, celebrity_adoption_tracker

load_dotenv()

# --- 1. LLM setup ---
llm = ChatOpenAI(
    model="openrouter/free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)

# --- 2. Tools ---
tools = [scrape_fashion_history, cycle_pattern_analyzer, celebrity_adoption_tracker]

# --- 3. Memory ---
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# --- 4. Prompt (tool-calling agents use a chat-style prompt, not raw text) ---
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Fashion Trend Time-Traveler agent. Given a garment "
               "or outfit description, use your tools to research its original "
               "era and its modern revival, then give a percentage breakdown "
               "across decades. "
               "IMPORTANT: Base your final answer ONLY on the exact information "
               "returned by your tools. Do NOT add celebrity names, brands, dates, "
               "or facts that were not explicitly present in the tool observations. "
               "If the tools returned limited data, say so honestly rather than "
               "inventing plausible-sounding details."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# --- 5. Build the tool-calling agent ---
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

# --- 6. Executor ---
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=6,
)