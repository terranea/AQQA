

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

    return prompt


if __name__ == "__main__":

    initial_instructions = """Your task is to transform natural language to a sparql query. 
    There are the following labels for observable attributes: CO, NO2, O3, PM10, PM2P5 SO2
    The full names of those attributes are: carbon_monoxide nitrogen_dioxide ozone particulate_matter_10um particulate_matter_2.5um sulphur_dioxide
    For the query always the short version has to be used.
    If you are not sure if you can construct the sparql query, respond <I am sorry, but I cannot create a sparql query from this question>
    The structure of this query is purposely divided in subqueries to improve performance. Don't change this structure."""


    nl_question_example_1 = "What was the <observable attribute> concentration in <location name> for <month> <year>?"
    sparql_query_example_1 = """
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX geo: <http://www.opengis.net/ont/geosparql#> 
    PREFIX gadm: <http://example.com/ontologies/gadm#>

    SELECT ?obs_result ?obs_time ?foi_ent
    WHERE {
        {
            SELECT ?foi_ent
            WHERE {
                ?foi_ent a sosa:FeatureOfInterest ;
                    geo:intersects ?gadm_ent .
                ?gadm_ent a gadm:AdministrativeUnit ;
                    gadm:hasName <location name> ;
                    gadm:hasNationalLevel 3 ;
            }
        }

        ?obs_ent a sosa:Observation ;
                sosa:hasSimpleResult ?obs_result ; 
                sosa:resultTime ?obs_time ;
                sosa:hasFeatureOfInterest ?foi_ent ;
                sosa:observedProperty ?obs_prop_ent .
        ?obs_prop_ent a sosa:ObservableProperty ;
            rdfs:label <observable attribute e.g. PM10> .

        FILTER (YEAR(?obs_time) = <year> && MONTH(?obs_time) = <mont>)
    }
    """

    nl_question_target = "List all observations where the ozone value was above 40 during summer 2020."

    prompt = generate_text_to_sparql_prompt(nl_question_target, 
                                            [nl_question_example_1], 
                                            [sparql_query_example_1], 
                                            initial_instructions=initial_instructions) 

    print(prompt)






