```python
python start.py
```
# Inventory
Create an inventory module. In the module-level namespace, define constants for the number of index partitions and document partitions you're going to use.
# Front-end Server
The front-end is a tornado server. It receives queries, coordinates the activities of the index and document servers, and returns a final result list. Upon receiving a query, the frontend sends it to each of the N index servers, and receives back N lists of (document ID, score) pairs. These lists are merged, and only the top K results are kept.
## API
### Request
```json
GET /search?q=query_here
```
### Response
```json
{"numResults": 3,
 "results": [{"title": "Result 1",
              "url": "http://...",
              "snippet": "Ipsum lorem bacon ..."},
             {"title": "Result 2",
              "url": "http://...",
              "snippet": "Ipsum lorem bacon ..."},   
             {"title": "Result 3",
              "url": "http://...",
              "snippet": "Ipsum lorem bacon ..."}]}
```
# Indexer
The indexer should read in a MediaWiki XML dump and output pickled data structures that can be read by the index and document servers. We're using document partitioning rather than term partitioning
# Index Server
## API
### Request
```json
GET /doc?id=doc_id_here&q=query_here
```
### Response
```json
{"results": [{"title": "Result 1",
              "url": "http://...",
              "snippet": "Ipsum lorem bacon ..."}]}
```






