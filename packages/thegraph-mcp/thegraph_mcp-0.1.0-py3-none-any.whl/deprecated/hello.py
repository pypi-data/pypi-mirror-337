import asyncio
import httpx
import os
from dotenv import load_dotenv
load_dotenv()

def json_to_graphql_schema(schema_json):
    """Convert JSON schema from introspection to GraphQL format."""
    types = schema_json["types"]
    schema_text = ""
    
    for t in types:
        if t["kind"] == "OBJECT" and not t["name"].startswith("__"):  # 排除内置类型
            schema_text += f"type {t['name']} {{\n"
            if t["fields"]:
                for f in t["fields"]:
                    field_type = f["type"]
                    type_name = field_type["name"]
                    if field_type["kind"] == "NON_NULL":
                        type_name = f"{field_type['ofType']['name']}!"
                    elif field_type["kind"] == "LIST":
                        type_name = f"[{field_type['ofType']['name']}]"
                    schema_text += f"  {f['name']}: {type_name}\n"
            schema_text += "}\n\n"
    
    return schema_text.strip()
    
async def test():
  THEGRAPH_API_BASE_URL = "https://gateway.thegraph.com/api/"
  THEGRAPH_API_KEY = os.getenv("THEGRAPH_API_KEY")
  subgraph_id = "5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV"

  client = httpx.AsyncClient() 
  url = f"{THEGRAPH_API_BASE_URL}{THEGRAPH_API_KEY}/subgraphs/id/{subgraph_id}"
  introspection_query = """
  query IntrospectionQuery {
    __schema {
      types {
        name
        kind
        fields {
          name
          type {
            name
            kind
            ofType {
              name
              kind
            }
          }
        }
      }
    }
  }
  """
  try:
      response = await client.post(url, json={"query": introspection_query}, timeout=10)
      response.raise_for_status()
      print(response.text)
      
      '''
      schema_data = response.json()
      schema_text = json_to_graphql_schema(schema_data["data"]["__schema"])
      print(schema_text)
      '''
  except httpx.HTTPError as e:
      return f"Error fetching schema: {str(e)}"
              
asyncio.run(test())              