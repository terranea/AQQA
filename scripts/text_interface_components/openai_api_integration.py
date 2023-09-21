import openai
from prompt_generation import generate_text_to_sparql_prompt


# set OPENAI_KEY as environment variables
# os.environ["OPENAI_KEY"] = "<OPENAI_KEY>"

# set OPENAI_KEY
#openai.api_key = os.environ["OPENAI_KEY"]

STRABON_ENDPOINT_URL = "http://64.225.134.139:9999/Strabon/Query"


def get_completion(prompt, model="gpt-3.5-turbo", temperature=0): 
    """use gpt model to generate text completion given a certain prompt"""

    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
    )
    return response.choices[0].message["content"]


def query_strabon_endpoint(sparql_query: str, endpoint_url: str = STRABON_ENDPOINT_URL):
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

    # generate sparql query from natural language question
    nl_questions_examples = []
    sparql_questions_examples = []
    target_questions = ""
    instructions = ""

    prompt = generate_text_to_sparql_prompt(target_question, nl_questions_examples, sparql_questions_examples, instructions)
    sparql_query = get_completion(prompt)

    # use sparql query for data retrieval from strabon
    response = query_strabon_endpoint(sparql_query)
    for row in response:
        print(row)




    



