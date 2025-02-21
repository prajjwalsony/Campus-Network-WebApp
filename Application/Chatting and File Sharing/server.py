from flask import Flask, request, jsonify, render_template
import IPListAccess, genIPList
import requests
import os
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
PORT = 3000 
CORS(app)

MESSAGE = [] #this will we equal to the id of the sender when receve something
FILE = [] #this will we equal to the id of the sender when receve something



UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




#FOR NOTIFICATION
@app.route('/status', methods=['GET'])
def status(MESSAGE=MESSAGE, FILE=FILE):
    # print(MESSAGE+FILE)
    try:
        message=""
        file=""
        if(len(MESSAGE) == 0):
            message = " : "
        else:
            message = f"{MESSAGE[0]}:{IPListAccess.getName(MESSAGE[0])}"
        if(len(FILE) == 0):
            file = " : "
        else:
            file = f"{FILE[0]}:{IPListAccess.getName(FILE[0])}"
        MESSAGE.clear()
        FILE.clear()
        return message+":"+file
    except:
        MESSAGE = ""
        FILE = ""
        return "ERROR"


#RETURN THE TABLE WITH ID-IP LIST TO SHOW TO THE USER IN FRONTEND
@app.route('/getNameIdList', methods=['GET'])
def getList():
    try:
        name, id = IPListAccess.getNameIdList()
        dictio = dict()
        for i in range(0, len(name)):
            dictio.update({str(id[i]):str(name[i])})
        return str(dictio)
    except:
        return "Cannot fetch ID-IP list"



#HOME PAGE
@app.route('/', methods=['GET'])
def start():
    return render_template("index.html")



#ADDING IP TO LIST, API FOR ADDING ID AND IP TO ID-IP TABLE MANUALLY BY USER
@app.route('/addIP', methods=['POST'])
def addip():
    try:
        ip=request.form.get('ip')
        name=request.form.get('name')
        # if ip == "":
        #     text, condition=scan(id)
        #     if condition == False:
        #         return 'Unable to Update. Try again..'
        #     else:
        #         return text
        try:
            id=request.form.get('id')
            IPListAccess.addIP(id, ip, name)
            return "IP added. Now Scan to update to Latest IP"
        except :
            IPListAccess.addIP(id, "", name)
            return "IP added. Now Scan to update to Latest IP"
    except:
        return "Cannot Add IP"
    



#API TO FETCH AND DISPLAY MESSAGES
@app.route('/showmsg', methods=['POST'])
def show1():
    try:
        id=request.form.get('id')
        # print("here: ",id)
        return render_template('showmsg.html', name=IPListAccess.getName(id), message=IPListAccess.getMessage(id))
    except:
        return "cannot show Message"



# API TO SEND MESSAGE(link destination IP, message). IT SEND THE MESSAGE BY MAKING THE GET REQUEST TO DESTINATION IP
@app.route('/sendText', methods=['POST'])
def send1():
    try:
        id=request.form.get('id')
        receiver_ip = IPListAccess.getIP(id)
        message=request.form.get('message')
        # print(f"POST to ID={id}, IP={receiver_ip} and message={message}")
        url = f'http://{receiver_ip}:{PORT}/receiveText?id={genIPList.MYID}&message={message}'
        try:
            response = requests.get(url, timeout=1)
            temp = response.text
            IPListAccess.addMessage(id, message, 'S')
            return temp
        except requests.RequestException as e:
            return f"Message cannot be delivered. The IP address {receiver_ip} is not found or may be changed"
    except:
        return "There is some error in sending Message"



#API TO CAPTURE THE MESSAGE WHICH IS BEING SENT ON THIS IP AND MAKE AN APPROPRIATE RESPONCE
@app.route('/receiveText')
def receive():
    try:
        id = request.args.get('id')
        ip = request.remote_addr
        message = request.args.get('message')
        # print(id, ip, message)
        IPListAccess.addIP(id, ip)
        IPListAccess.addMessage(id, message, 'R')
        # print(f"RECEIVED from ID={id}, IP={ip} and message={message}")
        MESSAGE.append(str(id))
        return "message_received"
    except:
        return "Receiver cannot process the message"



#SCANNING
def send_request(i):
    url = f'http://{i}:{PORT}/respond?id={genIPList.MYID}'
    # print(requests.get(url, timeout=2), end='\n')
    try:
        response = requests.get(url, timeout=2)
        # print(response.text)
        if (response.text).isdigit() == True:
            IPListAccess.addIP(response.text, i)
            return True # Indicating a successful request and response
        # print(f"IP= {i}  ID= {response.text}", end='\n')
        return False  # Indicating a successful request but unsuccessful response
    except requests.RequestException:
        pass
    # print(f"IP= {i}  ID= no response", end='\n')
    return False  # Indicating a failed request

@app.route('/scan', methods=['GET'])
def scan():
    try:
        ipList = genIPList.generate_IP_List()
        count = 0

        # Use ThreadPoolExecutor to run requests in parallel
        with ThreadPoolExecutor(max_workers=200) as executor:
            futures = [executor.submit(send_request, i) for i in ipList]

            for future in futures:
                if future.result():  # If the request was successful
                    count += 1

        return render_template("index.html", MESSAGE=str(f"Scan Completed. {count} contacts Updated")), False
        # return f"Scan Completed\n{count} contacts Updated", False 
    except:
        return "There is some Error during scanning!!!"



#API FOR SENDING FILE TO RECEIVER
# @app.route('/sendFile', methods=['POST'])
# def sendFile():
#     file = request.files['file']
#     id = request.form.get('id')
#     receiver_ip = IPListAccess.getIP(id) 



@app.route('/getIP', methods=['GET'])
def getip():
    try:
        id = request.args.get('id')
        IP = IPListAccess.getIP(id)
        return IP
    except:
        return "there is some error"


#API FOR RECEIVING THE FILE FROM SENDER
@app.route('/receiveFile', methods=['POST'])
def receiveFile():
    try:
        file = request.files['file']
        id = str(request.form.get('id'))
        if(id=="None"  or file=="None"):
            return "File received in Invalid Format"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], id+"__"+file.filename))
        # print("here")
        # print("File received")
        FILE.append(id)
        return "ACK from Receiver: File received succefully"
    except:
        # print("File not received")
        return "ACK from Receiver: There is some error"




#API FOR RESPONDING DURING SCANNING PROCESS BY A SENDER DEVICE
@app.route('/respond', methods=['GET'])
def respond():
    senderID = request.args.get('id')
    senderIP = request.remote_addr
    IPListAccess.addIP(senderID, senderIP)
    # print(f"RECEIVED from ID={senderID}, IP={senderIP} for scanning")
    return str(genIPList.MYID)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORT)
