from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Configuration for GitLab API
GITLAB_URL = 'http://your-self-hosted-gitlab-url'
PROJECT_ID = 'your-project-id'  # Replace with your project ID
PRIVATE_TOKEN = 'your-private-token'  # Replace with your private token

@app.route('/branches', methods=['GET'])
def get_branches():
    headers = {
        'Private-Token': PRIVATE_TOKEN,
    }
    response = requests.get(f'{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/repository/branches', headers=headers)
    
    if response.status_code == 200:
        branches = [branch['name'] for branch in response.json()]
        return jsonify(branches), 200
    else:
        return {'error': 'Failed to fetch branches'}, response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)