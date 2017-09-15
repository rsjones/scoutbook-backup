# Scoutbook Backup Script
Script written in python to back-up a unit's [Scoutbook](https://www.scoutbook.com) Scouts, "Scout Advancement", "Leaders & Parents", "Camping, Hiking, and Service Logs", and "Payment Logs" records to a local file and/or directly into Amazon AWS S3. Script can be run using AWS Lambda and run nightly using a CloudWatch event.

Tested with python 2.7

## Running Locally without AWS S3

1. Install [python](https://www.python.org/downloads/release/python-2713/), suggestion is to enable the option to add it to your path
1. Install python requests module `pip install requests -t .`
1. Open backup.bat if on Windows or backup.sh on linux
1. Replace <your_email> and <your_sb_password> with your Scoutbook login
1. Find your unit's Scoutbook id
    1. Open a browser and login to Scoutbook
	1. Navigate to your Unit's page
	1. In the address bar of the browser you'll find the parameter with the unit's id `https://www.scoutbook.com/mobile/dashboard/admin/unit.asp?UnitID=99999`
	1. Copy the numbers from the unit id
1. Replace the <your_unit_id> with the id from Scoutbook
1. Save the backup.bat or backup.sh
1. Double click the backup.bat on Windows or run the backup.sh on linux
1. A timestamped zip file should be written to the directory 

## Running Locally uploading to AWS S3

1. Install [python](https://www.python.org/downloads/release/python-2713/), suggestion is to enable the option to add it to your path
1. Install python requests module `pip install requests -t .`
1. Install python boto3 module to interact with AWS S3 `pip install boto3`
1. Configure your AWS credentials file, you can use the [AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html), profiles are supported.
1. Open backup.bat if on Windows or backup.sh on linux
1. Replace <your_email> and <your_sb_password> with your Scoutbook login
1. Find your unit's Scoutbook id
    1. Open a browser and login to Scoutbook
	1. Navigate to your Unit's page
	1. In the address bar of the browser you'll find the parameter with the unit's id `https://www.scoutbook.com/mobile/dashboard/admin/unit.asp?UnitID=99999`
	1. Copy the numbers from the unit id
1. Replace the <your_unit_id> with the id from Scoutbook
1. Change WRITE_S3=False to True
1. Enter the name of your S3 bucket, [don't know how?](http://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html)
1. (Optional) Remove the comment (REM or #) and set the name of the AWS profile from your credentials file
1. Save the backup.bat or backup.sh
1. Double click the backup.bat on Windows or run the backup.sh on linux
1. A timestamped zip file should be written to the directory