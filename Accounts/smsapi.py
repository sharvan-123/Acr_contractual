import requests
proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

#For Login
def loginOtp(mobile,otp):
	mobile = "8517007090"
	url = "https://resourceutils.mpcz.in:8888/MPCZ_OTP/api/otp/getOtp"
	payload = {"source": "Test App","mobileNo": str(mobile)}
	headers = {
		"Content-Type": "application/json",
		"Accept": "/",
		"Accept-Encoding": "gzip, deflate, br",
		"User-Agent": "EchoapiRuntime/1.1.0",
		"Connection": "keep-alive"
	}
	try:
		response = requests.request("POST", url, json=payload, headers=headers,verify=False)
		print(response.text)
		if response:return response.json()
	except:
		return {"status":True,"message":"Something Went Wrong "}
	
def verifyOtp(mobile,otp):
	mobile = "8517007090"
	url = "https://resourceutils.mpcz.in:8888/MPCZ_OTP/api/otp/verifyOtpAll"
	payload = {
		"mobileNo": str(mobile),
		"source": "Test App",
		"otp": str(otp)
	}
	headers = {
		"Accept": "/",
		"Accept-Encoding": "gzip, deflate, br",
		"User-Agent": "EchoapiRuntime/1.1.0",
		"Connection": "keep-alive",
		"Content-Type": "application/json"
	}
	try:
		response = requests.request("POST", url, json=payload, headers=headers,verify=False)
		print(response.text)
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

def reporting_sms(name,mobile, reviewingName):
	mobile = "8827053980"
	name = "Pawan Singh"
	reviewingName = "Sumit Parmar"
	message = "प्रिय "+str(name)+", आपकी ACR रिपोर्ट आपके रिपोर्टिंग अधिकारी द्वारा पूरी कर ली गई है और आपके समीक्षा अधिकारी "+str(reviewingName)+" को भेज दी गई है| Thank You. -MPMKVVCL BHOPAL"
	header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
	url = "https://api.pinnacle.in/index.php/sms/urlsms?sender=CCMPCZ&numbers="+str(mobile)+"&messagetype=TXT&message="+ str(message) +" &response=Y&dltentityid=1201158039515302745&apikey=210d59-4684c1-525x69-0e1352-5fde17&dlttempid=1007688303325051886"
	print(url,"123456")
	try:
		response = requests.get(url, proxies=proxyDict, headers=header)
		if response:return response.json()
	except:
		return {"status":True,"message":"Something Went Wrong"}
	
def reviewingOtp(name,mobile, AcceptingName):
	message =     "प्रिय "+str(name)+", आपकी ACR रिपोर्ट आपके पुनरीक्षण कर्ता अधिकारी द्वारा पूरी कर ली गई है और आपके स्वीकृतकर्ता अधिकारी "+str(AcceptingName)+" को भेज दी गई है । धन्यवाद. -MPMKVVCL BHOPAL"
	header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
	url = "https://sms.mpcz.in/api/v1/send-message?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160595139988353&message=" + str(message) + "&campaign=&mobile_numbers=" +str(mobile)+ "&message_type=1&route_type=0&schedule_date=&is_flash=0"
	try:
		response = requests.get(url, headers=header)
		if response:return response.json()
	except:
		return {"status":True,"message":"Something Went Wrong"}

def acceptingOtp(name,mobile, AcceptingName):
	message = "प्रिय "+str(name)+", आपकी ACR रिपोर्ट को स्वीकृतकर्ता अधिकारी "+str(AcceptingName)+" द्वारा सफलतापूर्वक अनुमोदित कर दिया गया है| धन्यवाद. -MPMKVVCL BHOPAL"
	header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
	url = "https://sms.mpcz.in/api/v1/send-message?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160595117506210&message=" + str(message) + "&campaign=&mobile_numbers=" +str(mobile)+ "&message_type=1&route_type=0&schedule_date=&is_flash=0"
	try:
		response = requests.get(url, headers=header)
		if response:return response.json()
	except:
		return {"status":True,"message":"Something Went Wrong"}

# import requests
# # def reportingOtp(name,mobile,session, reviewingName):
# message = "Dear sir, Your Appraisal Report for year has been completed by your Reporting Officer and forwarded next to your Reviewing Officer off2 l. Thank you. -MPMKVVCL BHOPAL"
# header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
# url = "https://sms.mpcz.in/api/v1/send-message?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160595156524521&message=" + str(message) + "&campaign=&mobile_numbers=" +str(8517007090)+ "&message_type=1&route_type=0&schedule_date=&is_flash=0"
# try:
# 	response = requests.get(url, headers=header)
# 	print(response)

	
# 	print("tru")
# except:
# 	print("false")

# 	# return {"status":True,"message":"Something Went Wrong"}
# name,mobile, reviewingName
# reporting_sms()