import uuid
from flask import Flask, request
from whatsapper.whatsapper import Whatsapper

app = Flask(__name__)

# Initialize a dictionary to store session IDs and corresponding Selenium instances
sessions = {}

@app.route('/open')
def load():
    # Create a new Selenium instance for this session
    selenium = Whatsapper()
    selenium.open_chrome()

    # Generate a new session ID and store the Selenium instance in the sessions dictionary
    session_id = str(uuid.uuid4())
    sessions[session_id] = selenium

    return {'session_id': session_id}

@app.route('/sessions')
def get_sessions():
    # Create a new Selenium instance for this session
    return [{'session_id': session_id} for session_id in sessions]



@app.route('/number')
def load_number():
    # Get the phone number, message, wait flag, and session ID from the request parameters
    phone = request.args.get('phone')
    message = request.args.get('message', default="", type=str)
    session_id = request.args.get('session_id')

    # Load the message for the specified session ID
    selenium = sessions.get(session_id)
    if not selenium:
        return {'error': 'Invalid session ID'}

    success = selenium.load_number(phone=phone, message=message)
    if success:
        return {'message': 'Number loaded'}
    else:
        return {'error': 'Failed to load number'}

@app.route('/write')
def write_message():
    # Get the phone number, message, wait flag, and session ID from the request parameters
    message = request.args.get('message')
    send = request.args.get('send', default=False, type=bool)
    session_id = request.args.get('session_id')

    # Load the message for the specified session ID
    selenium = sessions.get(session_id)
    if not selenium:
        return {'error': 'Invalid session ID'}

    success = selenium.write_message(message)
    if not success:
        return {'error': 'Problem writing message'}
    message = 'Wrote message'
    if send is True:
        success = selenium.send()
        message = 'Wrote and sent message'
    return {'message': message}

@app.route('/send')
def send():
    session_id = request.args.get('session_id')

    # Load the message for the specified session ID
    selenium = sessions.get(session_id)
    if not selenium:
        return {'error': 'Invalid session ID'}

    success = selenium.send()
    if not success:
        return {'error': 'Problem sending message'}
    return {'message': 'Sent message'}

@app.route('/close')
def close():
    # Get the session ID from the request parameters
    session_id = request.args.get('session_id')

    # Close the browser for the specified session ID
    selenium = sessions.get(session_id)
    if not selenium:
        return {'error': 'Invalid session ID'}

    selenium.close()

    # Remove the session from the dictionary of active sessions
    del sessions[session_id]

    return {'message': 'Browser closed successfully'}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
