import openai
import os
from SPARQLWrapper import SPARQLWrapper, JSON
from prompt_generation import generate_text_to_sparql_prompt
from config import STRABON_SPARQL_ENDPOINT, PATH_TO_OPENAI_KEY, PATH_TO_MODEL_INSTRUCTIONS


# set OPENAI_KEY
os.environ["OPENAI_KEY"] = open(PATH_TO_OPENAI_KEY, 'r').read()
openai.api_key = os.environ["OPENAI_KEY"]


def read_question_sparql_pair(path_to_ttl_file: str):
    """Reads sparql query from ttl file. First line should always contain the question in natural language"""

    with open(path_to_ttl_file, 'r') as ttl_file:
        lines = ttl_file.readlines()
    
    # Extract the NL question from the first line
    if lines:
        nl_question = lines[0].strip()

    # Extract the SPARQL query from the remaining lines
    if len(lines) > 1:
        sparql_query = ''.join(lines[1:])
    
    return nl_question, sparql_query
        

def get_completion(prompt, model="gpt-3.5-turbo", temperature=0): 
    """use gpt model to generate text completion given a certain prompt"""

    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
    )
    return response.choices[0].message["content"]


def query_strabon_endpoint(sparql_query: str, endpoint_url: str):
    """
    Execute a SPARQL query on a Strabon RDF triple store endpoint and retrieve data.

    Args:
        sparql_query (str): The SPARQL query to execute.
        endpoint_url (str): The URL of the Strabon RDF triple store endpoint.

    Returns:
        list or None: A list of query results or None if there was an error.
    """
    
    # Create a SPARQLWrapper object for the specified endpoint URL
    sparql = SPARQLWrapper(endpoint_url)

    # Set the SPARQL query
    sparql.setQuery(sparql_query)

    # Set the return format to JSON
    sparql.setReturnFormat(JSON)

    try:
        # Execute the query and get the results
        results = sparql.queryAndConvert()
        return results["results"]["bindings"]
    except Exception as e:
        # Print the error message for debugging purposes
        print(f"Error executing SPARQL query: {e}")
        return None


if __name__ == "__main__":

    instructions = open(PATH_TO_MODEL_INSTRUCTIONS, 'r').read()
    paths_to_sparql_queries = ["../sparql_queries/get_agg_cams_aq_values.ttl"]
    nl_questions_examples = []
    sparql_queries_examples = []

    target_question = "List all observations where the ozone value was above 40 during summer 2020."
    #target_question = "Give me the first 10 triples"

    # read sparql:question examples
    for path in paths_to_sparql_queries:
        nl_question, sparql_query = read_question_sparql_pair(path)
        nl_questions_examples.append(nl_question)
        sparql_queries_examples.append(sparql_query)
    
    prompt = generate_text_to_sparql_prompt(target_question, nl_questions_examples, sparql_queries_examples, instructions)

    # request to openai api to get sparql query for target question
    sparql_query = get_completion(prompt)
    print("---")
    print(sparql_query)
    print("---")

    # use sparql query for data retrieval from strabon
    response = query_strabon_endpoint(sparql_query, STRABON_SPARQL_ENDPOINT)

    # print out results
    for row in response:
        print(row)




    



