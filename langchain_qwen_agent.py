#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "langchain>=1.0",
#   "langchain-openai>=1.0",
# ]
# ///

"""Minimal LangChain create_agent example for the local llama.cpp server."""

import os

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI


@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


model = ChatOpenAI(
    model="Qwen3.5-9B-Q4_K_M.gguf",
    base_url=os.getenv("LLAMA_BASE_URL", "http://127.0.0.1:8080/v1"),
    api_key=os.getenv("LLAMA_API_KEY", "not-needed"),
    temperature=0,
)

agent = create_agent(
    model=model,
    tools=[add],
    system_prompt="You are a concise assistant. Use tools when useful.",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "23과 19를 더해줘."}]}
)
print(result["messages"][-1].content)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "23과 19를 더해줘."}]}
)
print(result["messages"][-1].content)
