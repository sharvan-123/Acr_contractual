import requests

#For Login
def loginOtp(mobile,otp):
	header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
	url = f"https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007282133448965289&mobile_number={mobile}&v1=ACR&v2={otp}"
	try:
		response = requests.get(url, headers=header)
		if response:return response.json()
	except:
		return {"status":True,"message":"Something Went Wrong "}
def appraiseeOtp(name,mobile,session):
	message = "Dear "+name+", Your ACR for "+str(session)+" has been submitted successfully and Forwarded to the Next Authority. - MPMKVVCL"
	header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
	url = "https://sms.mpcz.in/api/v1/send-message?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007361279894006110&message=" + str(message) + "&campaign=&mobile_numbers=" +str(mobile)+ "&message_type=1&route_type=0&schedule_date=&is_flash=0"
	try:
		response = requests.get(url, headers=header)
		if response:return response.json()
	except:
		return {"status":True,"message":"Something Went Wrong"}

def reportingOtp(name,mobile,session, reviewingName):
	message = "Dear "+str(name)+", Your Appraisal Report for year "+str(session)+" has been completed by your Reporting Officer and forwarded next to your Reviewing Officer "+str(reviewingName)+" l. Thank you. -MPMKVVCL BHOPAL"
	header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
	url = "https://sms.mpcz.in/api/v1/send-message?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160595156524521&message=" + str(message) + "&campaign=&mobile_numbers=" +str(mobile)+ "&message_type=1&route_type=0&schedule_date=&is_flash=0"
	try:
		response = requests.get(url, headers=header)
		if response:return response.json()
	except:
		return {"status":True,"message":"Something Went Wrong"}

def reviewingOtp(name,mobile,session, acceptingName):
	message =     "Dear "+str(name)+", your Appraisal Report for "+str(session)+" has been completed by your Reviewing Officer and forwarded next to your Accepting Officer "+str(acceptingName)+" . Thank you. -MPMKVVCL BHOPAL"
	header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
	url = "https://sms.mpcz.in/api/v1/send-message?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160595139988353&message=" + str(message) + "&campaign=&mobile_numbers=" +str(mobile)+ "&message_type=1&route_type=0&schedule_date=&is_flash=0"
	try:
		response = requests.get(url, headers=header)
		if response:return response.json()
	except:
		return {"status":True,"message":"Something Went Wrong"}

def acceptingOtp(name,mobile,session, acceptingName):
	message = "Dear "+str(name)+", the Appraisal Report "+str(session)+" has been successfully approved by Accepting Officer "+str(acceptingName)+" . Thank you. -MPMKVVCL BHOPAL"
	header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
	url = "https://sms.mpcz.in/api/v1/send-message?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160595117506210&message=" + str(message) + "&campaign=&mobile_numbers=" +str(mobile)+ "&message_type=1&route_type=0&schedule_date=&is_flash=0"
	try:
		response = requests.get(url, headers=header)
		if response:return response.json()
	except:
		return {"status":True,"message":"Something Went Wrong"}

