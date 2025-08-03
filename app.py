#this is my main entity agent file
import os
import getpass
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph.message import add_messages
from langchain_core.output_parsers import JsonOutputParser
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
import json
from langgraph.graph import StateGraph, START, END

#helper function to set enviroment variables
def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

#load the enviroment variable
load_dotenv()
_set_env("GOOGLE_API_KEY")

#initialize the llm chat model
llm = init_chat_model("google_genai:gemini-2.0-flash")

#Defining entity agent state, allow the agent to access and proccess the coming information at different stages
class EntityAgentState(TypedDict):
    """Represent the state of my entity graph."""
    messages: Annotated[list, add_messages]
    incoming_data: dict # the incoming data - format is in assignment instructions
    original_mapping: dict # this is the context for agent
    mapping_results: list # the final results with scores

# this key for entity agent to give llm a specialized prommpt
# I am going to use ChatPromptTemplate from langchain.prompts
promt_template = ChatPromptTemplate.from_messages([
    ("system", 
     """
    You are an expert Entity Agent tasked with intelligently mapping field from incoming JSON data to a pre-defined original product field mapping.

    You goal is to find best matching original fields for each incoming field, you must return up to 3 best-fit original fields along with a confidence score (a float between 0.0 and 1.0) for each match. The confidence score should reflect how well the field name and its content match the original field.

    Here is the incoming JSON data:
    {incoming_data}

    Here is the pre-defined original field mapping:
    {original_mapping}

    Your final output must be a JSON array where each object contains:
    - "incoming_field": The name of the  field from the incoming data.
    - "best_matches": A list of upto three objects, each with "original_field" and "confidence_score".
    """),
    ("user", "Please map the incoming JSON field to the original field mapping and return the resutls in the specified JSON format."),
])
# using placeholders like incoming_data & original_mapping will provide the context to my agent (llm)

#the agent node - main function that process the prompt
def entity_mapper_node(state: EntityAgentState):
    """
    A node in the graph that perform the entity mapping task.
    """

    incoming_data = state.get("incoming_data", {})
    original_mapping = state.get("original_mapping", {})
    messages = state["messages"]

    #bind the llm with prompts and output parser
    parser = JsonOutputParser()
    chain = promt_template | llm | parser 

    #invoke the llm with the contextual info
    result = chain.invoke({
        "incoming_data": json.dumps(incoming_data, indent=2),
        "original_mapping": json.dumps(original_mapping, indent=2),
        "messages": messages
    })


    # the results from the llm
    return {"mapping_results": result, "messages": [AIMessage(content=str(result))]}

#define the grapht with the entity stat
graph_builder = StateGraph(EntityAgentState)

# add the nodes
graph_builder.add_node("entity_mapper", entity_mapper_node)
graph_builder.add_edge(START, "entity_mapper")
graph_builder.add_edge("entity_mapper", END)

#compile the graph
graph = graph_builder.compile()

original_product_fields  = {
    "product_name": {
      "description": "Name of the product",
      "type": "string"
    },
    "entity_name": {
      "description": "Name of the product entity",
      "type": "string"
    },
    "description": {
      "description": "Detailed description of the product",
      "type": "string"
    },
    "created_at": {
      "description": "Timestamp when the product was created",
      "type": "datetime"
    },
    "date": {
      "description": "Timestamp when the product was registred",
      "type": "datetime"
    },
    "price": {
      "description": "Retail price of the product",
      "type": "float"
    }
  }
incoming_product_data =  [
    {
      "p_name": "Ultra Bottle",
      "desc": "High quality stainless steel bottle",
      "createdOn": "2023-04-12T10:00:00Z",
      "cost": 19.99
    }
  ]

#invoke the graph with the initialize state
initial_state = {
    "incoming_data": incoming_product_data,
    "original_mapping": original_product_fields,
    "messages": [HumanMessage(content="Please perform the field mapping")]
}

final_state = graph.invoke(initial_state) # type: ignore

# Print the final mapping results
print(final_state["mapping_results"])