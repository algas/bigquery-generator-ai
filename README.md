# bigquery-generator-ai

A tool to create a BigQuery SQL using natural language in ChatGPT.  
Just write the table name and what you want to achieve with the query, and SQL will be generated.  
It refers to the table schema instead of the data in the table to understand the data structure.

https://github.com/algas/bigquery-generator-ai

ChatGPT user registration is required to use it.
You will also need to configure your environment and download user credentials to run queries in BigQuery.

## Setup

1. Sign up for ChatGPT  
https://platform.openai.com/signup
1. Create a API Key of OpenAI (do not forget it)  
https://platform.openai.com/account/api-keys
1. Set up Google Cloud Credentials (save to `./google_credential.json`)  
https://cloud.google.com/docs/authentication/provide-credentials-adc
1. Set up BigQuery  
https://cloud.google.com/bigquery/docs/quickstarts/query-public-dataset-console

## Usage

```sh
docker run --rm -e OPENAI_API_KEY=_YOUR_API_KEY_ \
-e GOOGLE_APPLICATION_CREDENTIALS=/app/google_credential.json \
-v /path/to/credential:/app/google_credential.json \
-it algas/bigquery-generator-ai:latest \
'Instruction' \
'Bigquery Table' \
['Optional Bigquery Tables']
```

### Example

```sh
docker run --rm -e OPENAI_API_KEY=_YOUR_API_KEY_ \
-e GOOGLE_APPLICATION_CREDENTIALS=/app/google_credential.json \
-v $(PWD)/google_credential.json:/app/google_credential.json \
-it algas/bigquery-generator-ai:latest \
'Retrieve the names of customers who purchased products in March 2018.' \
'dbt-tutorial.jaffle_shop.customers' \
'dbt-tutorial.jaffle_shop.orders'
```

### Example Result

> Entering new LLMChain chain...
Prompt after formatting:

Write a BigQuery SQL that achieves the following.
```
Retrieve the names of customers who purchased products in March 2018.
```

The format of the target tables is as follows.
```json
[{"project": "dbt-tutorial", "dataset": "jaffle_shop", "table": "customers", "schema": [{"name": "ID", "type": "INTEGER", "mode": "NULLABLE"}, {"name": "FIRST_NAME", "type": "STRING", "mode": "NULLABLE"}, {"name": "LAST_NAME", "type": "STRING", "mode": "NULLABLE"}]}, {"project": "dbt-tutorial", "dataset": "jaffle_shop", "table": "orders", "schema": [{"name": "ID", "type": "INTEGER", "mode": "NULLABLE"}, {"name": "USER_ID", "type": "INTEGER", "mode": "NULLABLE"}, {"name": "ORDER_DATE", "type": "DATE", "mode": "NULLABLE"}, {"name": "STATUS", "type": "STRING", "mode": "NULLABLE"}, {"name": "_etl_loaded_at", "type": "DATETIME", "mode": "NULLABLE"}]}]
```

Example:
```sql
SELECT * FROM `project.dataset.table`;
```
    

> Finished chain.

Answer:
```sql
SELECT c.FIRST_NAME, c.LAST_NAME 
FROM `dbt-tutorial.jaffle_shop.customers` c 
INNER JOIN `dbt-tutorial.jaffle_shop.orders` o 
ON c.ID = o.USER_ID 
WHERE EXTRACT(MONTH FROM o.ORDER_DATE) = 3 
AND EXTRACT(YEAR FROM o.ORDER_DATE) = 2018;
```
