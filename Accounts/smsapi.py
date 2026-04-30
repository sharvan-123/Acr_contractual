import requests
proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

#For Login
def loginOtp(mobile,otp):
	# mobile = "8827053980"
	print(mobile,"mobile")
	url = "https://resourceutils.mpcz.in:8888/MPCZ_OTP/api/otp/getOtp"
	payload = {"source": "Contractual ACR","mobileNo": str(mobile)}
	headers = {
	'Content-Type': 'application/json'
	}
	try:
		response = requests.request("POST", url, json=payload, headers=headers,verify=False)
		print(response.text)
		if response:return response.json()
	except:
		return {"status":True,"message":"Something Went Wrong "}
	
def verifyOtp(mobile, otp):
    # mobile = "8827053980"
    url = "https://resourceutils.mpcz.in:8888/MPCZ_OTP/api/otp/verifyOtpAll"
    payload = {
        "mobileNo": str(mobile),
        "source": "Contractual ACR",
        "otp": str(otp)
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, verify=False)
        data = response.json()
        print("Response Code:", data.get("code"))
        return data
    except Exception as e:
        print("Error:", str(e))
        return None

def send_sms_reporting(name,mobile, reviewingName):
    message = f"प्रिय {name}, आपकी ACR रिपोर्ट आपके रिपोर्टिंग अधिकारी द्वारा पूरी कर ली गई है और आपके समीक्षा अधिकारी {reviewingName} को भेज दी गई है| धन्यवाद. -MPMKVVCL BHOPAL |"
    headers = {'Authorization': 'Bearer fJLnivwnxRXMrhck30MqtlKrw5IUhc15'}
    url = "https://msg.cerfgs.com/pushapi/sendmsg?username=MPMKVVCL_ERP&dest=91"+str(mobile)+"&apikey=rw7g17n0HsI5To0xhfKd6wX8OKY8OqYS&signature=CCMPCZ&msgtype=UNI&msgtxt="+ str(message) +"&entityid=1201158039515302745&templateid=1007688303325051886"
    print("url+++++++++++", url)
    try:
        response = requests.request("GET", url,proxies=proxyDict, headers=headers)
        print("response:", response.text)
        if response:
            return response.json()
    except Exception as e:
        print("error:", e)
        return {"status": True, "message": "Something Went Wrong"}


def send_sms_reviewing(name,mobile, ReviewingName):
    message = f"प्रिय {name}, आपकी ACR रिपोर्ट आपके पुनरीक्षण कर्ता अधिकारी द्वारा पूरी कर ली गई है और आपके स्वीकृतकर्ता अधिकारी {ReviewingName} को भेज दी गई है | धन्यवाद. -MPMKVVCL BHOPAL |"
    headers = {'Authorization': 'Bearer fJLnivwnxRXMrhck30MqtlKrw5IUhc15'}
    url = "https://msg.cerfgs.com/pushapi/sendmsg?username=MPMKVVCL_ERP&dest=91"+str(mobile)+"&apikey=rw7g17n0HsI5To0xhfKd6wX8OKY8OqYS&signature=CCMPCZ&msgtype=UNI&msgtxt="+ str(message) +"&entityid=1201158039515302745&templateid=1007600347917589168"
    print("url+++++++++++", url)
    try:
        response = requests.request("GET", url,proxies=proxyDict, headers=headers)
        print("response:", response.text)
        if response:
            return response.json()
    except Exception as e:
        print("error:", e)
        return {"status": True, "message": "Something Went Wrong"}


def send_sms_accepting(name, mobile, AcceptingName):
    message = f"प्रिय {name}, आपकी ACR रिपोर्ट को स्वीकृतकर्ता अधिकारी {AcceptingName} द्वारा सफलतापूर्वक अनुमोदित कर दिया गया है| धन्यवाद. -MPMKVVCL BHOPAL"
    headers = {'Authorization': 'Bearer fJLnivwnxRXMrhck30MqtlKrw5IUhc15'}
    url = "https://msg.cerfgs.com/pushapi/sendmsg?username=MPMKVVCL_ERP&dest=91"+str(mobile)+"&apikey=rw7g17n0HsI5To0xhfKd6wX8OKY8OqYS&signature=CCMPCZ&msgtype=UNI&msgtxt="+ str(message) +"&entityid=1201158039515302745&templateid=1007435805364665975"
    print("url+++++++++++", url)
    try:
        response = requests.request("GET", url,proxies=proxyDict, headers=headers)
        print("response:", response.text)
        if response:
            return response.json()
    except Exception as e:
        print("error:", e)
        return {"status": True, "message": "Something Went Wrong"}
        
# mobile = "8827053980"
# name = "Pawan Payasi"
# reviewingName = "Tina Sharma"

# send_sms_reporting(name,mobile,reviewingName)
# send_sms_reviewing(name,mobile,reviewingName)
# send_sms_accepting(name,mobile,reviewingName)
