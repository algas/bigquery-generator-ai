# bigquery-generator-ai

A tool to create a BigQuery SQL using natural language in ChatGPT.  
Just write the table name and what you want to achieve with the query, and SQL will be generated.  
It refers to the table schema instead of the data in the table to understand the data structure.

https://github.com/algas/bigquery-generator-ai

ChatGPT user registration is required to use it.
You will also need to configure your environment and download user credentials to get the table schema in BigQuery.

## Setup

### ChatGPT API

1. Sign up for ChatGPT  
https://platform.openai.com/signup
1. Create a API Key of OpenAI (do not forget it)  
https://platform.openai.com/account/api-keys
1. Set your API key to the enviromnent variable  
`export OPENAI_API_KEY=xxxxxx`

### Google Cloud

1. Set up BigQuery  
https://cloud.google.com/bigquery/docs/quickstarts/query-public-dataset-console
1. Create a service account  
https://cloud.google.com/iam/docs/service-accounts-create
1. Apply "BigQuery Metadata Viewer" (roles/bigquery.metadataViewer) role to the service account  
https://cloud.google.com/bigquery/docs/access-control#bigquery.metadataViewer  
https://cloud.google.com/iam/docs/manage-access-service-accounts#grant-single-role
1. Create a service account key (and save to `./credential.json`)  
https://cloud.google.com/iam/docs/keys-create-delete#iam-service-account-keys-create-console
1. Set the path to the credential file to the enviromnent variable  
`export GOOGLE_APPLICATION_CREDENTIALS=$PWD/credential.json`

## Usage

```sh
docker run --rm -e OPENAI_API_KEY=$OPENAI_API_KEY \
-e GOOGLE_APPLICATION_CREDENTIALS=/app/credential.json \
-v $GOOGLE_APPLICATION_CREDENTIALS:/app/credential.json \
-it algas/bigquery-generator-ai:latest \
'Instruction' \
'Bigquery Table' \
['Optional Bigquery Tables']
```

### Example

```sh
docker run --rm -e OPENAI_API_KEY=$OPENAI_API_KEY \
-e GOOGLE_APPLICATION_CREDENTIALS=/app/credential.json \
-v $GOOGLE_APPLICATION_CREDENTIALS:/app/credential.json \
-it algas/bigquery-generator-ai:latest \
'Retrieve the names of customers who purchased products in March 2018.' \
'dbt-tutorial.jaffle_shop.customers' \
'dbt-tutorial.jaffle_shop.orders'
```

### Example Result

```sql
SELECT c.FIRST_NAME, c.LAST_NAME 
FROM `dbt-tutorial.jaffle_shop.customers` c 
INNER JOIN `dbt-tutorial.jaffle_shop.orders` o 
ON c.ID = o.USER_ID 
WHERE EXTRACT(MONTH FROM o.ORDER_DATE) = 3 
AND EXTRACT(YEAR FROM o.ORDER_DATE) = 2018;
```

## Build

If you want to run your code in your own python environment without docker, the following steps are required.

1. Clone the git reposigory  
`git clone https://github.com/algas/bigquery-generator-ai.git`
1. Install dependencies  
`pip install -r requirements.txt`
1. Run a script
```sh
python bq_sql_gen.py \
'Retrieve the names of customers who purchased products in March 2018.' \
'dbt-tutorial.jaffle_shop.customers' \
'dbt-tutorial.jaffle_shop.orders'
```

## Note

- Adding `-v` or `--verbose` at the end of the command will also output the contents of the prompt.
- It may not output correct SQL if complex instructions or statements unrelated to the query are given.
