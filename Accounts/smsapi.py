import requests
proxyDict = {"http": "proxy1.mpcz.in:8080", "https": "proxy1.mpcz.in:8080"}

#For Login
def loginOtp(mobile,otp):
	# mobile = "8517007090"
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
	# mobile = "8517007090"
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

# def reporting_sms():
# 	mobile = "918827053980"
# 	name = "Pawan"
# 	reviewingName = "Sumit"
# 	# message = "प्रिय "+str(name)+", आपकी ACR रिपोर्ट आपके रिपोर्टिंग अधिकारी द्वारा पूरी कर ली गई है और आपके समीक्षा अधिकारी "+str(reviewingName)+" को भेज दी गई है| Thank You. -MPMKVVCL BHOPAL"
# 	# message = "प्रिय "+str(name)+", आपकी ACR रिपोर्ट आपके रिपोर्टिंग अधिकारी द्वारा पूरी कर ली गई है और आपके समीक्षा अधिकारी "+str(reviewingName)+" को भेज दी गई है| धन्यवाद. -MPMKVVCL BHOPAL"
# 	# message = "प्रिय सुमित कुमार, आपकी ACR रिपोर्ट आपके रिपोर्टिंग अधिकारी द्वारा पूरी कर ली गई है और आपके समीक्षा अधिकारी सुरेश कुमार को भेज दी गई है| धन्यवाद. -MPMKVVCL BHOPAL"
# 	header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
# 	# url = "https://api.pinnacle.in/index.php/sms/urlsms?sender=CCMPCZ&numbers=8517007090&messagetype=UNI&message="+ str(message) +" &response=Y&dltentityid=1201158039515302745&apikey=210d59-4684c1-525x69-0e1352-5fde17&dlttempid=1007688303325051886"
# 	url="https://api.pinnacle.in/index.php/sms/urlsms?sender=CCMPCZ&numbers=9926286466&messagetype=UNI&message=प्रिय सुमित कुमार, आपकी ACR रिपोर्ट आपके रिपोर्टिंग अधिकारी द्वारा पूरी कर ली गई है और आपके समीक्षा अधिकारी सुरेश कुमार को भेज दी गई है| धन्यवाद. -MPMKVVCL BHOPAL |&response=Y&dltentityid=1201158039515302745&apikey=210d59-4684c1-525x69-0e1352-5fde17&dlttempid=1007688303325051886"
# 	print(url,"123456")
# 	# try:
# 	response = requests.get(url, proxies=proxyDict, headers=header, verify=False)
# 	if response:return response.json()
# # except:
# 	return {"status":True,"message":"Something Went Wrong"}
	
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



# def send_sms():
# 			mobile = "918827053980"
# 			name = "Pawan"
# 			reviewingName = "Sumit"
#             message = f"प्रिय सुमित कुमार, आपकी ACR रिपोर्ट आपके रिपोर्टिंग अधिकारी द्वारा पूरी कर ली गई है और आपके समीक्षा अधिकारी सुरेश कुमार को भेज दी गई है| धन्यवाद. -MPMKVVCL BHOPAL |"
# 			message = f"प्रिय "+str(name)+", आपकी ACR रिपोर्ट आपके रिपोर्टिंग अधिकारी द्वारा पूरी कर ली गई है और आपके समीक्षा अधिकारी "+str(reviewingName)+" को भेज दी गई है| धन्यवाद. -MPMKVVCL BHOPAL |"
#             # Construct the URL for sending the SMS
#             url = f"https://api.pinnacle.in/index.php/sms/urlsms?sender=CCMPCZ&numbers=8827053980&messagetype=UNI&message={message}&response=Y&dltentityid=1201158039515302745&apikey=210d59-4684c1-525x69-0e1352-5fde17&dlttempid=1007688303325051886"
#             # url = f"https://api.pinnacle.in/index.php/sms/urlsms?sender=CCMPCZ&numbers={officer_data.cug_mobile}&messagetype=TXT&message={message}&response=Y&dltentityid=1201158039515302745&apikey=03695d-0794d5-53e943-7x06a9-93ab48&dlttempid=1007674889182348523"
            
#             # Define proxy settings (if necessary)
#             proxyDict = {"http": "proxy1.mpcz.in:8080", "https": "proxy1.mpcz.in:8080"}
            
#             # Send the SMS request
#             sms_response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'}, verify=False)
            
#             # Check the response status
#             if sms_response.status_code == 200:
#                 response_content = sms_response.text  # Get the response content as text
#                 # SmsLog.objects.create(mobile_number=officer_data.cug_mobile, message=message, response_message=response_content)
#                 return {"message": "SMS sent successfully."}  # Return success message
#             else:
#                 return {"error": f"Failed to send SMS. Status code: {sms_response.status_code}."}  # Log the error response
#         # except Officer.DoesNotExist:
#             return {"error": "Officer not found."}  # Handle the case where the officer is not found
#         # except ApplicantDetails.DoesNotExist:
#             return {"error": "Applicant not found."}  # Handle the case where the applicant is not found
#     # else:
#     #     return {"error": "Mobile number is missing."}  # Handle missing mobile number

# # reporting_sms()
# send_sms()

import requests
import urllib.parse

def send_sms_reporting(name,mobile, reviewingName):
    # mobile = "918827053980"
    # name = "Pawan"
    # reviewingName = "Sumit"
    # Compose Hindi message
    message = f"प्रिय {name}, आपकी ACR रिपोर्ट आपके रिपोर्टिंग अधिकारी द्वारा पूरी कर ली गई है और आपके समीक्षा अधिकारी {reviewingName} को भेज दी गई है| धन्यवाद. -MPMKVVCL BHOPAL |"

    # URL encode the Hindi text
    encoded_message = urllib.parse.quote(message)

    # Construct SMS API URL
    url = (
        f"https://api.pinnacle.in/index.php/sms/urlsms?"
        f"sender=CCMPCZ&numbers={mobile}&messagetype=UNI&message={encoded_message}"
        f"&response=Y&dltentityid=1201158039515302745"
        f"&apikey=210d59-4684c1-525x69-0e1352-5fde17"
        f"&dlttempid=1007688303325051886"
    )

    # Define proxy settings (if your office network requires it)
    proxyDict = {
        "http": "http://proxy1.mpcz.in:8080",
        "https": "http://proxy1.mpcz.in:8080"
    }

    # Send the SMS request
    try:
        sms_response = requests.get(
            url,
            proxies=proxyDict,
            headers={"User-Agent": "Mozilla/5.0"},
            verify=False,
            timeout=15
        )
        if sms_response:return sms_response.json()
        else:
            print("Response:", sms_response.text)
    except Exception as e:
        print("Unexpected error:", e)


def send_sms_reviewing(name,mobile, AcceptingName):
    message = f"प्रिय {name}, आपकी ACR रिपोर्ट आपके पुनरीक्षण कर्ता अधिकारी द्वारा पूरी कर ली गई है और आपके स्वीकृतकर्ता अधिकारी {AcceptingName} को भेज दी गई है | धन्यवाद. -MPMKVVCL BHOPAL |"
    # URL encode the Hindi text
    encoded_message = urllib.parse.quote(message)
    # Construct SMS API URL
    url = (
        f"https://api.pinnacle.in/index.php/sms/urlsms?"
        f"sender=CCMPCZ&numbers={mobile}&messagetype=UNI&message={encoded_message}"
        f"&response=Y&dltentityid=1201158039515302745"
        f"&apikey=210d59-4684c1-525x69-0e1352-5fde17"
        f"&dlttempid=1007600347917589168"
    )
    # Define proxy settings (if your office network requires it)
    proxyDict = {
        "http": "http://proxy1.mpcz.in:8080",
        "https": "http://proxy1.mpcz.in:8080"
    }

    # Send the SMS request
    try:
        sms_response = requests.get(
            url,
            proxies=proxyDict,
            headers={"User-Agent": "Mozilla/5.0"},
            verify=False,
            timeout=15
        )

        if sms_response.status_code == 200:
            print("Response:", sms_response.text)
        else:
            print("Response:", sms_response.text)

    except Exception as e:
        print(" Unexpected error:", e)

# send_sms_reviewing()


def send_sms_accepting(name,mobile, AcceptingName):
    message = f"प्रिय {name}, आपकी ACR रिपोर्ट को स्वीकृतकर्ता अधिकारी {AcceptingName} द्वारा सफलतापूर्वक अनुमोदित कर दिया गया है| धन्यवाद. -MPMKVVCL BHOPAL"
    encoded_message = urllib.parse.quote(message)
    # Construct SMS API URL
    url = (
        f"https://api.pinnacle.in/index.php/sms/urlsms?"
        f"sender=CCMPCZ&numbers={mobile}&messagetype=UNI&message={encoded_message}"
        f"&response=Y&dltentityid=1201158039515302745"
        f"&apikey=210d59-4684c1-525x69-0e1352-5fde17"
        f"&dlttempid=1007435805364665975"
    )

    # Define proxy settings (if your office network requires it)
    proxyDict = {
        "http": "http://proxy1.mpcz.in:8080",
        "https": "http://proxy1.mpcz.in:8080"
    }
	
    # Send the SMS request
    try:
        print(url)
        sms_response = requests.get(
            url,
            proxies=proxyDict,
            headers={"User-Agent": "Mozilla/5.0"},
            verify=False,
            timeout=15
        )

        if sms_response.status_code == 200:
            print("Response:", sms_response.text)
        else:
            print("Response:", sms_response.text)

    except Exception as e:
        print(" Unexpected error:", e)
        
# send_sms_accepting()