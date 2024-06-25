# TODO: revisit API
from flask import Flask, jsonify

app = Flask(__name__)

# Sample data
data = {
    'message': 'Hello, this is a GET API response!'
}

# Define a route for the GET API endpoint
@app.route('/drug/get_example', methods=['GET'])
def get_example():
    return jsonify(data)

if __name__ == '__main__':
    # Run the application on localhost:5000
    app.run(debug=True)