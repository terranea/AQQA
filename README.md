# Air Quality Knowledge Graph with CAMS Data

This project aims to create an Air Quality Knowledge Graph using data from the Copernicus Atmosphere Monitoring Service (CAMS) and provide accessibility through natural language queries. At a high level, the project consists of three components working together to achieve this goal.

## Components Overview

1. **aq_kg_creation**: Data Acquisition and RDF Conversion
   - **Objective**: Convert CAMS Air Quality data into RDF format.
   - **Description**: This component handles the acquisition and conversion of CAMS data into RDF, making it suitable for integration into semantic web applications. It ensures the data is available for advanced querying and visualization.
   
2. **aq_kg_query**: RDF Data Storage and Querying
   - **Objective**: Prepare the Strabon RDF store for data storage and querying.
   - **Description**: This component guides you through the setup of the Strabon RDF store, data storage, and querying. Strabon serves as the database for storing and retrieving RDF data efficiently.
   
3. **aq_kg_text_interface**: Text-to-SPARQL with OPENAI API
   - **Objective**: Convert natural language text into SPARQL queries for data retrieval.
   - **Description**: This component provides the necessary code and files to leverage the OPENAI API for converting natural language text into SPARQL queries. It allows users to query the Air Quality Knowledge Graph using human-friendly language.

For detailed documentation on each component, refer to their respective folders.
