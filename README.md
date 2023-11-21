# Elasticsearch Index Inspector

The Elasticsearch Index Inspector is a Python script designed to interact with an Elasticsearch cluster, retrieving detailed information about its indices. It focuses on collecting data such as node distribution, read-only status, Index Lifecycle Management (ILM) phases, policy details, and the timestamp of the last document for each index. It uses environment variables for configuration to ensure secure and flexible setup.

## Features

- Connects to Elasticsearch using configurable environment variables.
- Skips indices with specified prefixes.
- Retrieves detailed information on each index, including node distribution, read-only status, ILM phase, policy, and last document timestamp.
- Outputs data in a structured JSON format.

## Prerequisites

- Python 3.x
- Elasticsearch Python client (`elasticsearch` package)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/morgan-atwood/elasticsearch-index-inspector.git
```
3. Navigate to the cloned directory:
```bash
cd elasticsearch-index-inspector
```
3. Install the required package:
```bash
pip3 install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the root directory of the project with the following content:
```
ES_ENDPOINT=https://your_elasticsearch_endpoint:9200
ES_USERNAME=your_username
ES_PASSWORD=your_password
```

Replace the placeholders with your Elasticsearch cluster's actual endpoint, username, and password.

2. Ensure that the `.env` file is included in your `.gitignore` to prevent uploading sensitive information to a public repository.

## Usage

Run the script:

```bash
python3 main.py
```
The script will output the details to indices_details.json.
