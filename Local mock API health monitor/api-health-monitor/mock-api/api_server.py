from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

# Counter to simulate intermittent failures
request_count = 0

@app.route('/health', methods=['GET'])
def health_check():
    """
    Basic health endpoint - always returns healthy status
    """
    return jsonify({
        'status': 'healthy',
        'service': 'mock-api',
        'timestamp': time.time()
    }), 200

@app.route('/api/users', methods=['GET'])
def get_users():
    """
    Simulates a user data endpoint with occasional failures
    """
    global request_count
    request_count += 1
    
    # Simulate failure every 5th request
    if request_count % 5 == 0:
        return jsonify({'error': 'Database connection failed'}), 500
    
    # Simulate slow response occasionally
    if request_count % 3 == 0:
        time.sleep(2)
    
    return jsonify({
        'users': ['alice', 'bob', 'charlie'],
        'count': 3
    }), 200

@app.route('/api/data', methods=['GET'])
def get_data():
    """
    Another endpoint with random response times
    """
    # Random delay between 0.1 and 1 second
    time.sleep(random.uniform(0.1, 1.0))
    
    return jsonify({
        'data': 'sample data',
        'processed': True
    }), 200

if __name__ == '__main__':
    print("Starting Mock API on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
