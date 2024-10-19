from flask import Flask, request
from signalwire.rest import Client as SignalWireClient
from signalwire.voice_response import VoiceResponse
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017")
db = client["dental_clinic"]
appointments_collection = db["appointments"]

# SignalWire Setup
project_id = '78d95212-bb86-446e-afba-fad79db384e7'  # Replace with your project ID
auth_token = 'PT5a51cc2d51fc8f84a2bba89292f1f840ca884a563eac238f'  # Replace with your auth token
space_url = 'techwizard.signalwire.com'  # Replace with your space URL
signalwire_client = SignalWireClient(project_id, auth_token, signalwire_space_url=space_url)

@app.route("/", methods=['GET'])
def home():
    return "Flask is running!"

@app.route("/voice", methods=['POST'])
def voice():
    response = VoiceResponse()
    response.say("Welcome to XYZ Dental Clinic. How can I assist you today?")
    response.redirect("/handle_request")
    return str(response)

@app.route("/handle_request", methods=['POST'])
def handle_request():
    user_input = request.form.get('SpeechResult', "")
    response = VoiceResponse()
    
    if "book an appointment" in user_input.lower():
        response.say("Please provide the date for your appointment.")
        # Logic for handling the appointment date
    elif "services" in user_input.lower():
        services_info = "We offer a variety of dental services including cleanings, fillings."
        response.say(services_info)
    elif "speak to a human" in user_input.lower():
        response.say("Connecting you to a human representative.")
    else:
        response.say("I didn't understand that. Please repeat.")
    
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
