# Scoutbook Backup Script
Script written in python to back-up a unit's [Scoutbook](https://www.scoutbook.com) Scouts, "Scout Advancement", "Leaders & Parents", "Camping, Hiking, and Service Logs", and "Payment Logs" records to a local file and/or directly into Amazon AWS S3. Script can be run using AWS Lambda and run nightly using a CloudWatch event.

Tested with python 2.7, to install [python](https://www.python.org/downloads/release/python-2713/), suggestion is to enable the option to add it to your path

## Running Locally without AWS S3

1. Download or Clone repository
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

1. Download or Clone repository
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

## Running in AWS Lambda uploading to AWS S3

1. Download or Clone repository
1. Install python requests module `pip install requests -t .`
1. Zip all folders installed and the backup.py
1. Login to the AWS console
1. Create a Lambda Function
1. Select Author from Scratch
1. Add a trigger or add it later, click next
1. Name your function e.g. scoutbook-backup ^ Select runtime of Python 2.7
1. Choose Upload a .ZIP file from the Code entry type dropdown
1. Click Upload button and select the created zip file
1. Create Environment variables for S3_BUCKET, PASSWORD, UNITID, WRITE_S3, EMAIL
1. Change the Lambda function Handler to backup.backup
1. Choose create a custom role from the role dropdown, this will open a new window
1. Give the role a name e.g lambda_scoutbook
1. Add AmazonS3FullAccess policy to the IAM Role
1. Back in the Lambda configuration page, Expand Advanced & set timeout to be 1 min
1. click next
1. Run Test to verify your lambda function
