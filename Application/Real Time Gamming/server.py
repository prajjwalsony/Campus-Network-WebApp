from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import requests

app = Flask(__name__)
CORS(app)
PORT = 5000 
STATUS = {'current': "", 'selected': ""}
PLAYED = {"from": "", "to": ""}

@app.route('/updateGameStatus', methods=['GET'])
def updateGameStatus():
    try:
        gameStatus = request.args.get('gameStatus')
        PLAYED.update(eval(gameStatus))
        return "UPDATED" 
    except Exception as e:
        return str(e)

@app.route('/receiveGameStatus', methods=['GET'])
def receiveGameStatus():
    return jsonify(PLAYED)

@app.route('/updateCurrentSituation', methods=['GET'])
def updateCurrentSituation():
    try:
        currentSituation = request.args.get('currentSituation')
        STATUS.update(eval(currentSituation))
        return "UPDATED"
    except Exception as e:
        return str(e)

@app.route('/receiveCurrentSituation', methods=['GET'])
def receiveCurrentSituation():
    return jsonify(STATUS)

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=PORT)
