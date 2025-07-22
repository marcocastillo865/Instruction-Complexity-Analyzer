# AI4ALL-Project

## Perfect Retriver Checklist Generator

### Core Idea:
Instead of building a search system to find the right article, assume you’ve already found it. Focus entirely on making the checklist generation perfect.

### Revised Goal: 
Given a specific wikiHow article, can an LLM reliably and accurately generate a simple, sequential checklist?

### Workflow:
1) Build a simple web interface
2) The user selects a wikiHow article from a pre-populated dropdown list (e.g., 20-30 articles chosen from the dataset)
3) Your backend feeds the full text of that selected article to an LLM (like open-source Llama 3 or Mistral) with a well-engineered prompt.
4) The LLM generates the checklist, which is then displayed to the user.
