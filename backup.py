from requests import session
import re
import zipfile
import datetime
import boto3
import StringIO

def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
  return datetime.datetime.now().strftime(fmt).format(fname=fname)

def getExportFile(c, url, filename, zf):
	response = c.get(url)
	
	zf.writestr(filename, response.content)

def backup(event=None, context=None):
	email = None
	password = None
	unitID = None
	isWriteDisk = False
	isWriteS3 = False
	bucketName = None
	profileName = None
	try:
		# This reads env variables in AWS Lambda style
		process
		email = process.env.EMAIL
		password = process.env.PASSWORD
		unitID = process.env.UNITID
		isWriteDisk = process.env.WRITE_DISK == "True"
		isWriteS3 = process.env.WRITE_S3 == "True"
		bucketName = process.env.S3_BUCKET
		profileName = process.env.AWS_PROFILE
	except NameError:
		# This reads env variables from os environment variables
		import os
		email = os.environ.get('EMAIL')
		password = os.environ.get('PASSWORD')
		unitID = os.environ.get('UNITID')
		isWriteDisk = os.environ.get('WRITE_DISK') == "True"
		isWriteS3 = os.environ.get('WRITE_S3') == "True"
		bucketName = os.environ.get('S3_BUCKET')
		profileName = os.environ.get('AWS_PROFILE')

	backupScoutBook(email, password, unitID, isWriteDisk, isWriteS3, bucketName, profileName)
	
def backupScoutBook(email, password, unitID, isWriteDisk=False, isWriteS3=False, bucketName=None, profileName=None):
	payload = {
		'Action': 'Login',
		'Email': email,
		'password': password
	}
	
	with session() as c:
		response = c.post('https://www.scoutbook.com/mobile/login.asp')
		
		searchObj = re.search( r'CSRF" value="(.*)"', response.content, re.M|re.I)
		csrf = searchObj.group(1)
		
		payload['CSRF'] = csrf
		
		c.post('https://www.scoutbook.com/mobile/login.asp?Source=&Redir=', data=payload)

		in_memory_zip = StringIO.StringIO()
		try:
			zf = zipfile.ZipFile(in_memory_zip, "w", zipfile.ZIP_DEFLATED, False)
			
			getExportFile(c, 'https://www.scoutbook.com/mobile/dashboard/admin/unit.asp?UnitID=' + unitID + '&Action=ExportScouts', 'ExportScouts.csv', zf)
				
			getExportFile(c, 'https://www.scoutbook.com/mobile/dashboard/admin/unit.asp?UnitID=' + unitID + '&Action=ExportAdvancement', 'ExportAdvancement.csv', zf)
			
			getExportFile(c, 'https://www.scoutbook.com/mobile/dashboard/admin/unit.asp?UnitID=' + unitID + '&Action=ExportAdults', 'ExportAdults.csv', zf)
			
			getExportFile(c, 'https://www.scoutbook.com/mobile/dashboard/admin/unit.asp?UnitID=' + unitID + '&Action=ExportLogs', 'ExportLogs.csv', zf)
			
			getExportFile(c, 'https://www.scoutbook.com/mobile/dashboard/admin/unit.asp?UnitID=' + unitID + '&Action=ExportPaymentLogs', 'ExportPaymentLogs.csv', zf)
						
		finally:
			zf.close()
		
		zipFileName = timeStamped('pack_backup.zip')

		if isWriteDisk == True:
			in_memory_zip.seek(0)
			f = file(zipFileName, "wb")
			f.write(in_memory_zip.read())
			f.close()

		if isWriteS3 == True:
			in_memory_zip.seek(0)
			
			sessions3 = boto3.Session(profile_name=profileName)
			# Any clients created from this session will use credentials
			# from the [dev] section of ~/.aws/credentials.
			s3 = sessions3.client('s3')
			s3.upload_fileobj(in_memory_zip, bucketName, zipFileName, ExtraArgs={'StorageClass': 'STANDARD_IA'})
		
# Script start 
if __name__ == "__main__":
	backup()