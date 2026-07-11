
from flask import Flask, jsonify
import requests
from gitlab import GitLab

app = Flask(__name__)

def get_branches():
    url = 'https://gitlab.example.com/api/v4/projects/<project_id>/repository/branches'
    headers = {'PRIVATE-TOKEN': '<private_token>'}
    response = requests.get(url, headers=headers)
    branches = response.json()

    # Extract just the names of the branches
    branch_names = [branch['name'] for branch in branches]

    return branch_names

@app.route('/branches', methods=['GET'])
def branches_api():
    branch_names = get_branches()
    return jsonify(branch_names)

if __name__ == '__main__':
    app.run(debug=True)