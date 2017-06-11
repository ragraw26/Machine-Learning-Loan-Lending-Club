#!/bin/bash

DECLINED=$1

if [ -z $DECLINED ]; then
    echo "Working on LendingClub Data-1"
    python3 /src/PART1-downloader_luigi.py featureSelection --local-scheduler --loginemail $USERNAME --loginpassword $PASSWD
    mv /src/CleanedFile.csv /src/Output/
    mv /src/FeatureSelection.csv /src/Output/
else
    echo "Working on Declined Data-2"
    python3 PART1-declined_luigi.py FeatureSelection --local-scheduler --loginemail $USERNAME --loginpassword $PASSWD
    mv /src/CleanedRejectLoan.csv /src/Output/
    mv /src/RejectCorrelation.csv /src/Output/
fi

find .

if [ $? -eq 0 ]
then
  echo "Successfully created the files now going to upload them in S3"
  sh /src/awsS3Upload.sh
else
  echo "Could not create file" >&2
fi
