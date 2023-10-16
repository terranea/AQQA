import rdflib
from config import PATH_TO_MODEL_INSTRUCTIONS

def generate_text_to_sparql_prompt(target_question: str, 
                                   example_questions: list, 
                                   example_sparql_queries: list, 
                                   initial_instructions: str):
    """
    Generate a prompt context with Natural Language questions and SPARQL queries.

    Args:
        example_questions (list): A list of Natural Language questions.
        example_sparql_queries (list): A list of SPARQL queries corresponding to the questions.
        initial_instructions (str): Initial instructions for the prompt.

    Returns:
        str: The formatted prompt.
    """
    prompt = initial_instructions + "\n\n"

    for i, (nl_question, sparql_query) in enumerate(zip(example_questions, example_sparql_queries), start=1):
        prompt += f"<Natural Language> (Question {i}):\n{nl_question}\n\n"
        prompt += f"<SPARQL Query> (Question {i}):\n{sparql_query}\n\n"
    prompt += f"<Natural Language> (Target Question):\n{target_question}\n\n"
    prompt += f"<Sparql Query> (Target Question):"

    return prompt


if __name__ == "__main__":


    # query all sparql queries in queries.ttl and their description which have the predicate "isForPrompt"
    # Load the RDF data from the "queries.ttl" file
    g = rdflib.Graph()
    g.parse("queries.ttl", format="turtle")

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

    # define question of interest
    nl_question_target = "List all observations where the ozone value was above 40 during summer 2020."

    # create query
    prompt = generate_text_to_sparql_prompt(nl_question_target, 
                                        example_descriptions,
                                        example_queries, 
                                        model_instructions) 

    print(prompt)





