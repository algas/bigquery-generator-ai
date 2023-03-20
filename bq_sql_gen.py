import sys
import os
from langchain import PromptTemplate, OpenAI, LLMChain
from google.cloud import bigquery
import json

TEMPLATE = '''
Write a BigQuery SQL that achieves the following.
```
{{ content }}
```

The format of the target tables is as follows.
```json
{{ schema }}
```

Example:
```sql
SELECT * FROM `project.dataset.table`;
```
    '''

def get_schema(table_name: str) -> str:
    client = bigquery.Client()
    table = client.get_table(table_name)
    project_id = table.project
    dataset_id = table.dataset_id
    table_id = table.table_id
    schema = list(map(lambda x: x.to_api_repr(), table.schema))
    return {'project':project_id,'dataset':dataset_id,'table':table_id,'schema':schema}

def get_schemas(table_names: list[str]):
    return json.dumps([get_schema(n) for n in table_names])

def predict(content: str, table_names: list[str]):
    prompt = PromptTemplate(
        input_variables=["content","schema"],
        template=TEMPLATE,
        template_format='jinja2',
    )
    llm_chain = LLMChain(
        llm=OpenAI(temperature=0), 
        prompt=prompt, 
        verbose=True
    )
    return llm_chain.predict(content=content, schema=get_schemas(table_names))

if __name__ == '__main__':
    content = sys.argv[1]
    table_names = sys.argv[2:]
    print(predict(content, table_names))
