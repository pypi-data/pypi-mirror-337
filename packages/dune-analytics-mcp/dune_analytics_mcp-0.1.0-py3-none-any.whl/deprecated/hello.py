from dune_client.client import DuneClient
from dotenv import load_dotenv
load_dotenv()

dune = DuneClient.from_env()
query_result = dune.get_latest_result_dataframe(4853921)
print(query_result.to_csv())

#curl -H "X-Dune-API-Key:qp6AiPg7wUft2LoUoCWRVHQxx6YNZR51" "https://api.dune.com/api/v1/query/3623384/results?limit=1000"