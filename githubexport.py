import requests
import json
# import imp
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('.env')
# config = dotenv_values(".env")

class NotFoundException(Exception):
    def __init__(self, message, code):
        self._message = message
        self._code = code
        print(self.__cause__)
        super(message)

parent = Path(__file__).parent
file_path = parent / 'github.json'

class GithubExportService:


    url = "https://api.github.com/users/Akorede28"
    owner = "akorede28"
    repo = "e-commerce-API"
    commit_sha = os.getenv('commit_sha')
    

    def get_commit_request(self,  owner, repo):

        commit_url = f"https://api.github.com/repos/{owner}/{repo}/commits"

        response = requests.get(commit_url)

        if(str(response.status_code).startswith('4')):
            i = 0

            while i < 3:
                response = requests.get(commit_url)
                i += 1
                break
            raise NotFoundException('no repo found', 404)

       
        print(response.json())
        return response

    def get_pull_request(self, owner, repo, commit_sha):
        
        pull_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}/pulls"

        response = requests.get(pull_url)

        if(str(response.status_code).startswith('4')):
            i = 0

            while i < 3:
                response = requests.get(pull_url)
                i += 1
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
url = github.url
own = github.owner
rep = github.repo
sha = github.commit_sha

res = github.get_commit_request(own, rep)
pull = github.get_pull_request(own, rep, sha)
github.make_file(res)



