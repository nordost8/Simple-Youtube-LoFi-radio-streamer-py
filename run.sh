#!/bin/bash

nohup -u python video_master.py > video_master_log.txt 2>&1 &

nohup -u python translation_master.py > translation_master_log.txt 2>&1 &