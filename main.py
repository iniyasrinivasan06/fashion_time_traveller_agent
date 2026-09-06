"""
main.py
Entry point. Runs the Fashion Trend Time-Traveler agent on one or more
queries. Because the same agent_executor/memory is reused across calls
in the same run, the agent retains short-term memory across questions.
"""

from agent import agent_executor


def ask(query: str):
    print(f"\n{'=' * 60}\nQUESTION: {query}\n{'=' * 60}")
    response = agent_executor.invoke({"input": query})
    print(f"\n--- FINAL ANSWER ---\n{response['output']}\n")


if __name__ == "__main__":
    ask("What decade is 'kerchief' from, and when did they get revived? Give a percentage breakdown.")

    # Uncomment to test short-term memory with a follow-up in the same run:
    # ask("What about chunky sneakers?")