#!/bin/sh
source ~/venv/bin/activate
cd ./assignment5
python reformatter.py info_ret.xml --jobPath=i_df_jobs --numPartitions=5
python reformatter.py info_ret.xml --jobPath=df_jobs --numPartitions=5
python reformatter.py info_ret.xml --jobPath=idf_jobs --numPartitions=5
