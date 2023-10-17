# Instructions for Using the OpenAI API to Convert Text to SPARQL Queries

These instructions will guide you through the process of utilizing the Language Model (LLM) from OpenAI via their API to transform natural language text into SPARQL queries. These queries can then be used to retrieve data from our Strabon database.

## Key Components 

1. **config.py**
Stores paths to neccesary files and URL for strabon endpoint

2. **model_instructions.txt**
This file stores the instructions for the task of the model. 

3. **queries.ttl**
This file stores the SPARQL queries which serve the OpenAI model as examples. How to include a SPARQL query in the prompt will be explained in one of the following steps.

4. **openai_text_to_sparql.py**
Code for creating the prompt and using the OpenAI model to convert text to SPARQL queries.


## Step 0: Get an OpenAI API key

Before you begin, ensure that you have obtained an OpenAI API key.

## Step 1: Configure paths

In the **config.py** file make sure that the paths defined correctly point to the required files on your local machine.

## Step 2: Adjust model instructions if neccesary

The current model instructions are:


- Your task is to generate SPARQL queries from natural language input. 
- Observable attributes are represented by the labels CO, NO2, O3, PM10, PM2P5, and SO2. Their full names are carbon_monoxide, nitrogen_dioxide, ozone, particulate_matter_10um, particulate_matter_2.5um, and sulfur_dioxide. Use the short versions of these labels in your queries.
- Do not allow queries that involve data updates or deletions. If such a query is encountered, respond with "<I am sorry, but I cannot create a SPARQL query from this question>"
- If you are uncertain about your ability to construct a SPARQL query, please respond with "<I am sorry, but I cannot create a SPARQL query from this question>."
- The query structure is intentionally divided into subqueries to enhance performance. Do not modify this structure.
- Right now data is only available for Austria and Bavaria. If the user asks for values outside those regions respond with 
<I am sorry, but data from {requested region} is not available at the moment>.

If you want the model to have different instructions you can directly adjust the **model_instructions.txt** file. 


## Step 3: Edit Examples to Include in the Prompt

In the queries.ttl file, you will find exemplary SPARQL queries defined. Each example includes at least the following predicates:

- **:hasQuery**: Defines the SPARQL query of the example.
- **:hasDescription**: Defines the corresponding description of the SPARQL query.
Optionally, some examples have the following predicates:

- **:isWorking**: ['True', 'False'] - Defines if a SPARQL query works and retrieves the correct results when run against the SPARQL endpoint.
- **:isForPrompt**: ['True', 'False'] - Defines if a Query:Description pair should be included in the model prompt. Both predicates must be set to 'True' for the examples to be included in the prompt.


## Step 4: Transform Text to Sparql queries

The **openai_text_to_sparql.py** file contains a function called **text_to_sparql**:

```python
def text_to_sparql(target_question: str):

    # prompt is generated from model instructions, examples and target question
    prompt = generate_text_to_sparql_prompt(target_question)

    # LLM is used to create a sparql query for the target question
    sparql_query = get_completion(prompt)

    return sparql_query
```

This function takes a target question as input, generates a prompt, and uses the Language Model to obtain the corresponding SPARQL query.
By following these steps, you can effectively convert natural language text into SPARQL queries for querying your Strabon database.





