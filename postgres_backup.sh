#!/bin/bash


#####################
# Author: Taofeecoh
# Date: 06/11/2025
#
#
#####################
source ./.env

docker exec -it farm_news-db-1 pg_dump -U ${DB_USER} -d ${DB_NAME} > ./pg_dump/farmtech$(date +"%Y-%m-%d_%H:%M")backup_dump.sql
echo "backup complete"