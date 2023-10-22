#!/bin/bash

nohup python video_master.py > video_master_log.txt 2>&1 &
nohup python translation_master.py > translation_master_log.txt 2>&1 &
