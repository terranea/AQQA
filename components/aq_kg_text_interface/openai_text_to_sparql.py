import openai
import os
import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON
from .config import STRABON_SPARQL_ENDPOINT, PATH_TO_OPENAI_KEY, PATH_TO_MODEL_INSTRUCTIONS, PATH_TO_QUERIES

# set OPENAI_KEY
os.environ["OPENAI_KEY"] = open(PATH_TO_OPENAI_KEY, 'r').read()
openai.api_key = os.environ["OPENAI_KEY"]


def generate_text_to_sparql_prompt(target_question: str):
    """creating prompt for openai model from model instructions, examples and question of interest. Output is str"""


    g = rdflib.Graph()
    g.parse(PATH_TO_QUERIES, format="turtle")

    # Define the SPARQL query
    query = """
    PREFIX aqqa: <http://example.com/ontologies/aqqa#> 

    SELECT ?queryText ?description
    WHERE {
    ?query aqqa:hasQuery ?queryText ;
            aqqa:hasDescription ?description ;
            aqqa:isWorking 'True' ;
            aqqa:isForPrompt 'True' .
    }
    """

    # Execute the SPARQL query
    results = g.query(query)

    example_queries = []
    example_descriptions = []

    # Print the results
    for row in results:
        query_text = row.queryText.toPython()
        example_queries.append(query_text)
        description = row.description.toPython()
        example_descriptions.append(description)

    # load model instructions
    model_instructions = open(PATH_TO_MODEL_INSTRUCTIONS, "r", encoding="utf-8").read()

    prompt = model_instructions + "\n\n"

    for i, (nl_question, sparql_query) in enumerate(zip(example_descriptions, example_queries), start=1):
        prompt += f"<Natural Language> (Question {i}):\n{nl_question}\n\n"
        prompt += f"<SPARQL Query> (Question {i}):\n{sparql_query}\n\n"
    prompt += f"<Natural Language> (Target Question):\n{target_question}\n\n"
    prompt += f"<Sparql Query> (Target Question):"

    return prompt


def get_completion(prompt, model="gpt-3.5-turbo", temperature=0): 
    """use gpt model to generate text completion given a certain prompt"""

    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
    )
    return response.choices[0].message["content"]


def text_to_sparql(target_question: str):

    # prompt is generated from model instructions, examples and target question
    prompt = generate_text_to_sparql_prompt(target_question)

    # LLM is used to create a sparql query for the target question
    sparql_query = get_completion(prompt)

    return sparql_query




if __name__ == "__main__":

    # define target question
    target_question = "List all observations where the ozone value was above 40 during summer 2020."

    # convert natural language to sparql query
    sparql_query = text_to_sparql(target_question)
        
    print("---")
    print(sparql_query)
    print("---")






    



