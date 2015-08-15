To Professor: 

To start workers, use:
python workers.py

-- The number of workers could be change in the workers.MAX_WORKER field
-- Port information will be logged on the console

To start coordinator, use:
python coordinator.py --mapperPath=wordcount/mapper.py --reducerPath=wordcount/reducer.py \
    --jobPath=oas_jobs --numReducers=1

To get the result, call the 'coordiator' handler on the given port:

http://linserv2.cims.nyu.edu:25799/coordinator?mapperPath=wordcount/mapper.py&reducerPath=wordcount/reducer.py&jobPath=oas_jobs&numReducers=1

-- In my assignment, my base port for coordinator is 25799 and base port for workers starts from 25800. Could be changed in the module
-- I use a tornado server as the coordinator, thus the route 'coordinator' should be called to fulfil its task. 