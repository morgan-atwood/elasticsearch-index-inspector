from elasticsearch import Elasticsearch
import json
import os

ES_ENDPOINT = os.getenv('ES_ENDPOINT')
ES_USERNAME = os.getenv('ES_USERNAME')
ES_PASSWORD = os.getenv('ES_PASSWORD')

es = Elasticsearch(
    ES_ENDPOINT,
    basic_auth=(ES_USERNAME, ES_PASSWORD)
)

# List of prefixes to skip
skip_prefixes = ['.ds-.fleet-actions-result', 'another_prefix', 'yet_another_prefix']

def get_index_info(es):
    indices_info = es.cat.indices(format='json')
    indices_details = {}

    for index_info in indices_info:
        index_name = index_info['index']

        # Skip indices based on the defined prefixes
        if any(index_name.startswith(prefix) for prefix in skip_prefixes):
            continue

        # Get shard information to find the node
        shards_info = es.cat.shards(index=index_name, format='json')
        nodes = set(shard['node'] for shard in shards_info if 'node' in shard)


        settings = es.indices.get_settings(index=index_name)
        index_settings = settings[index_name]['settings']['index']

        # Check if the 'blocks' key exists and if 'write' within it is set to 'true'
        is_read_only = index_settings.get('blocks', {}).get('write', 'false') == 'true'

        # Get ILM phase
        ilm_status = es.ilm.explain_lifecycle(index=index_name)
        ilm_phase = ilm_status['indices'][index_name].get('phase')
        ilm_policy_name = ilm_status['indices'][index_name].get('policy')

        last_doc_timestamp = get_last_document_timestamp(es, index_name)

        indices_details[index_name] = {
            'nodes': list(nodes),
            'is_read_only': is_read_only,
            'ilm_phase': ilm_phase,
            'ilm_policy_name' : ilm_policy_name,
            'last_document_timestamp': last_doc_timestamp
        }

    return indices_details


def get_last_document_timestamp(es, index_name, timestamp_field='@timestamp'):
    try:
        response = es.search(
            index=index_name,
            body={
                "query": {"match_all": {}},
                "sort": [{timestamp_field: {"order": "desc"}}],
                "size": 1
            }
        )
        if response['hits']['hits']:
            return response['hits']['hits'][0]['_source'].get(timestamp_field)
        return None
    except Exception as e:
        print(f"Error getting last document timestamp for index {index_name}: {e}")
        return None



# Get indices details
indices_details = get_index_info(es)

# Convert to JSON and write to a file
json_output = json.dumps(indices_details, indent=4)
with open('indices_details.json', 'w') as file:
    file.write(json_output)

print("Results written to indices_details.json")
