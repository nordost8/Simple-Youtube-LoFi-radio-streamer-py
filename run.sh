#!/bin/bash

# Запускаємо скрипт для генерації відео
python video_master.py &

# Запускаємо скрипт для трансляції на YouTube
python translation_master.py