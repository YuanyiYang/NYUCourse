```python
python start.py
```
# High-Level Overriew
### Offline Component

The indexer reads a WIKI XML dump and outputs pickled data structures that can be used by the index and documents servers. These data structures are:
1) inverted index: a dict that maps from term to a list of document IDs
2) document store: a dict that maps from document ID to the title, URL, and text of the document

### Online Components

The frontend server receives queries. When it receives one, it will forward it to each of the index servers. These index servers find in their respective inverted indices the document ID. They use TF-IDF scores to compute similarity and return the document IDs. The frontend receives and merges the ranked document ID lists from the index partitions. Then, for the highest documents, the frontend requests detailed data(title, URL and snippet) from the appropriate document partition.

# Implementation 
## Inventory
Create an inventory module. In the module-level namespace, define constants for the number of index partitions and document partitions will be used.

## Front-end Server
The front-end is a tornado server. It receives queries, coordinates the activities of the index and document servers, and returns a final result list. Upon receiving a query, the frontend sends it to each of the N index servers, and receives back N lists of (document ID, score) pairs. These lists are merged, and only the top K results are kept.

### API
#### Request
```json
GET /search?q=query_here
```
#### Response
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

## Indexer
The indexer should read in a MediaWiki XML dump and output pickled data structures that can be read by the index and document servers. We're using document partitioning rather than term partitioning

## Index Server
An index server is a Tornado HTTP server. It first uses the document frequency table to create a vector-space representation of the query. Each dimension of the vector should be set to the corresponding term's TF-IDF value. 
### API
#### Request
```json
GET /index?q=query_here
```
#### Response
```json
{"postings": [[231, 28.60], [186, 9.53]]}
```

## Document Servers
A document server is also a Tornado HTTP server. 
### API
#### Request
```json
GET /doc?id=doc_id_here&q=query_here
```
#### Response
```json
{"results": [{"title": "Result 1",
              "url": "http://...",
              "snippet": "Ipsum lorem bacon ..."}]}
```







