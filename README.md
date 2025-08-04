# Entity Agent

**Entity Agent** is a LangGraph-based tool that intelligently maps fields from incoming JSON data to a pre-defined product field schema. Leveraging a large language model, it analyzes both field names and content to provide accurate matches with confidence scores.

---

## Features

- **Intelligent Field Mapping:** Uses Gemini 2.0 Flash LLM to semantically match fields between different data schemas.
- **Confidence Scoring:** Assigns a confidence score (0.0 to 1.0) to each match, indicating mapping certainty.
- **Flexible Output:** Returns a JSON array with the best-fit original fields for each incoming field.
- **Graph Visualization:** Generates a PNG diagram visualizing the agent's workflow.

---

## Prerequisites

- **Python:** Version 3.8 or higher
- **Google API Key:** Required for accessing Google's generative models
- **Python Libraries:**  
   Install dependencies with:
  ```bash
  pip install langchain langgraph langchain_google_genai python-dotenv pygraphviz pydot
  ```

---

## Usage

1. **Clone the repository:**

   ```bash
   git clone git@github.com:emhamza/entity_agent.git
   cd entity-agent
   ```

2. **Set up your environment:**

   - Create a `.env` file in the project root and add your Google API Key:
     ```
     GOOGLE_API_KEY="your_api_key_here"
     ```

3. **Run the agent:**
   ```bash
   python app.py
   ```

---

## Output

- The terminal will display a JSON array with the mapping results.
- A file named `entity_agent_graph.png` will be saved in the project directory, visualizing the agent's workflow.

---

## License

This project is licensed under the [MIT License](./LICENSE).
