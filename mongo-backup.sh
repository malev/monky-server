#!/bin/bash
#Force file syncronization and lock writes

mongo admin --eval "printjson(db.fsyncLock())"

S3CONFIG_PATH="/home/deploy/.s3cfg"
MONGODUMP_PATH="/home/deploy/backup"
MONGO_HOST="localhost"
MONGO_PORT="27017"
MONGO_DATABASE="mapa76"

TIMESTAMP=`date +%F-%H%M`
S3_BUCKET_NAME="src.codingnews.info"
S3_BUCKET_PATH="mongodb-backups"


# Create backup
cd $MONGODUMP_PATH
mongodump -h $MONGO_HOST:$MONGO_PORT -d $MONGO_DATABASE

# Add timestamp to backup
mv dump mongodb-$HOSTNAME-$TIMESTAMP
tar cvzf mongodb-$HOSTNAME-$TIMESTAMP.tar.gz mongodb-$HOSTNAME-$TIMESTAMP

# Upload to S3
s3cmd put mongodb-$HOSTNAME-$TIMESTAMP.tar.gz s3://$S3_BUCKET_NAME/$S3_BUCKET_PATH/mongodb-$HOSTNAME-$TIMESTAMP.tar.gz -c $S3CONFIG_PATH

# Remove backup
rm -rf mongodb-$HOSTNAME-$TIMESTAMP
rm mongodb-$HOSTNAME-$TIMESTAMP.tar.gz

# Unlock databases writes
mongo admin --eval "printjson(db.fsyncUnlock())"
