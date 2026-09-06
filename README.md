# Fashion Trend Time-Traveler Agent

A ReAct-based AI agent that researches a garment's original era and
modern revival using an LLM (via OpenRouter), 3 custom tools
(web scraping + analysis), and short-term memory.

## Setup

1. Install dependencies:
pip install -r requirements.txt


2. Create a `.env` file in the project root (copy `.env.example`):

OPENROUTER_API_KEY=your_actual_key_here

Get a free key at https://openrouter.ai/keys

3. Run:

python main.py

## What it does

Given a garment/style (e.g. "mom jeans"), the agent:
1. Scrapes fashion history for its original era
2. Analyzes decade mentions to build a percentage breakdown
3. Tracks celebrity adoption to find the modern revival period
4. Synthesizes all findings into a final answer

## Tools used
- `scrape_fashion_history` — web search for garment origin
- `cycle_pattern_analyzer` — counts decade mentions, computes %
- `celebrity_adoption_tracker` — finds revival years via celebrity mentions
