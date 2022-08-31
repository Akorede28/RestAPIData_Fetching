from distutils.command.config import config
import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('.env')
parent = Path(__file__).parent
file_path = parent / 'github.json'

class NotFoundException(Exception):
    def __init__(self, message, code):
        self._message = message
        self._code = code
        super().__init__(message, code)


class Config:
    url = os.getenv('URL')
    owner = os.getenv('OWNER')
    repo = os.getenv('REPO')
    commit_sha = os.getenv('commit_sha')

    commit_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    pull_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}/pulls"


class GithubExportService:

    def get_commit_request(self, commit_url):

        response = requests.get(commit_url)

        if(str(response.status_code).startswith('4')):
            i = 0

            while i <= 3:
                response = requests.get(commit_url)
                i += 1
                print(i, "commit")
                break
            raise NotFoundException('no repo found', 404)      
        print(response.json())
        return response

    def get_pull_request(self, pull_url):
        
        response = requests.get(pull_url)

        if(str(response.status_code).startswith('4')):
            i = 0

            while i <= 3:
                response = requests.get(pull_url)
                i += 1
                print(i, "pull")
                break
            raise NotFoundException('no repo found', 404)
        print(response.json())
        return response

    
    def make_file(self, response):
          if file_path.exists:
            with open(file_path, 'w') as f:
                 json.dump(response.json(), f)
          else:
            with open(file_path, 'x') as f:
                    json.dump(response.json(), f)



github = GithubExportService()
config = Config()

res = github.get_commit_request(config.commit_url)
pull = github.get_pull_request(config.pull_url)
github.make_file(res)



