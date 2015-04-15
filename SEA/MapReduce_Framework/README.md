# High-Level Overview
The canonical \"word count\" example application.
## Frameworks vs. Application
This framework will be interface-compatible with Hadoop\'s streaming interface, so it\'ll be able to run many other MapReduce applications as well.
## Workers vs. Coordinator
Workers are Tornado HTTP servers that can perform either reduce or map tasks. The coordinator is a command-line Python program that invokes the workers
## Partitioning Strategy
Keys are assigned to reducers by hashing the key (modulo number of reducers).
## Life-Cycle of a Job
The coordinator takes as input a mapper program, a reducer program, the job\'s working directory (used for input files as well as output files), and the number of reducers (N) to use.

First, the coordinator searches the working directory for files that match the pattern \"*.in\", such as 0.in, 1.in, etc. These files are inputs to the MapReduce application. For each of the M input files, a mapper task is run.

Each mapper task takes as input a mapper program, an input file (such as 0.in), and the number of reducers (N) that will be used. The mapper task runs the mapper program against the input file, producing a list of key-value pairs, and then partitions the keys across the N reducers that will be run. This partitioning is performed by hashing the key (modulo N). This results in N lists of key-value pairs for each mapper task. These N lists are associated with a mapper task ID (unique to the mapper task) and stored in memory. Each mapper task returns its map task ID to the coordinator.

When the mapper tasks finish, the coordinator starts the N reducer tasks.

Each reducer task takes as input a reducer program, the map task IDs (M of them), the reducer\'s index (a value in the range [0 ... N-1]), and the job\'s working directory. The reducer first fetches its key-value pairs directly from each of the mappers. It then runs the reducer program against this input data, and writes the output to a file in the job\'s working directory (such as 0.out). The reducer\'s index (a value in the range [0 ... N-1]) is used to name the output file.

# Inventory
In the module-level namespace, define the URLs of each of your workers. Each worker should use a separate process. Each worker should listen on a single port and should be able to handle any type of request (map or reduce).

# Coordinator
The coordinator is a Python program that exposes a command-line interface. It coordinates the activities of the mapper and and reducer servers. For each of the M input files, a mapper task is run. Mapper tasks are assigned to workers in a round-robin fashion. When the mapper tasks finish, the reducer tasks are run. Reducer tasks are assigned to workers in a round-robin fashion as well. Each reducer task writes its output to a file. When the reducer tasks finish, the coordinator exits.

## CLI
### Command
```python
python coordinator.py \
    --mapperPath=wordcount/mapper.py \
    --reducerPath=wordcount/reducer.py \
    --jobPath=fish_jobs \
    --numReducers=1
```
### Output
numReducers output files should be written under jobPath.

# Mapper
The N output lists from the map task must not be overwritten if the same process is used to run another map task before the first task\'s outputs are retrieved. To distinguish outputs corresponding to different map tasks, a unique mapTaskID is generated for each task, and the N output lists are associated with this mapTaskID.

## Map API
### Request
```json
GET /map?
  mapperPath=wordcount/mapper.py&
  inputFile=fish_jobs/0.in&
  numReducers=1
```
### Response
```json
{"status": "success", "mapTaskID": "6a75d424315ba28ecdd901976b7833e8"}
```
## RetrieveMapOutput API
### Request
```json
GET /retrieveMapOutput?
  reducerIx=0&
  mapTaskID=6a75d424315ba28ecdd901976b7833e8
```
### Response
```json
[["fish", "1"], ["fish", "1"], ["one", "1"], ["two", "1"]]
```

# Reducer
The reducer module consists of a single Tornado RequestHandler. First, the reducer fetches its input data from the mappers. This process of moving map outputs to the reducers is known as shuffling. For each of the M map task IDs given, the reducer calls RetrieveMapOutput on the corresponding mapper, passing along the map task ID and reducer index. The mapper returns the sorted list of key-value pairs that correspond to the given map task ID and this particular reducer\'s partition.

Next, the reducer merges the M sorted lists of key-value pairs into a single list sorted by key.

Finally, the reducer program is run with the sorted list piped in through stdin. The reducer program\'s stdout is piped directly to an output file (such as jobPath/0.out, where 0 is the index of the reducer task).

## Reduce API
### Request
```json
GET /reduce?
  reducerIx=0&
  reducerPath=wordcount/reducer.py&
  mapTaskIDs=mapTaskID1,mapTaskID2&
  jobPath=fish_jobs
```
### Response
```json
{"status": "success"} 
```json

```python
python workers.py
``` 
All of the workers should start, and the URL of each should be logged to the console.
```python
python coordinator.py --mapperPath=wordcount/mapper.py --reducerPath=wordcount/reducer.py \
    --jobPath=oas_jobs --numReducers=1
```
A single output file (oas_jobs/0.out) should be written, consisting of a list of word counts sorted by word.


