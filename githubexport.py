from distutils.command.config import config
from random import random
from urllib import response
import requests
import json
import os
# import csv
import time
from pathlib import Path
from dotenv import load_dotenv
from pyspark.sql import *
from transforms import transform
# from tenacity import retry
import retry

# spark = SparkSession.builder.getOrCreate()
# spark.sparkContext.setLogLevel("WARN")


load_dotenv('.env')
parent = Path(__file__).parent
file_path = parent / 'github.json'

def retry(func, retries=3):
    def retry_wrapper(*args, **kwargs):
        attempts = 0
        while attempts < retries:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                print(e)
                time.sleep(2)
                attempts += 1
                print(attempts, "DONE")
    return retry_wrapper

# class NotFoundException(Exception):
#     def __init__(self, message, code):
#         self._message = message
#         self._code = code
#         super().__init__(message, code)


class Config:
    url = os.getenv('URL')
    owner = os.getenv('OWNER')
    repo = os.getenv('REPO')
    commit_sha = os.getenv('commit_sha')

    commit_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    pull_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}/pulls"


class GithubExportService:
    @retry
    def get_commit_request(self, commit_url):

        response = requests.get(commit_url)

        # if(str(response.status_code).startswith('4')):
        #     i = 0

        #     while i <= 3:
        #         response = requests.get(commit_url)
        #         i += 1
        #         print(i, "commit")
        #         break
        #     # raise NotFoundException('no repo found', 404)      
        print(response.json())
        return response
    
    @retry
    def get_pull_request(self, pull_url):
        
        response = requests.get(pull_url)

        # if(str(response.status_code).startswith('4')):
        #     i = 0

        #     while i <= 3:
        #         response = requests.get(pull_url)
        #         i += 1
        #         print(i, "pull")
        #         break
        #     raise NotFoundException('no repo found', 404)
        print(response.json())
        return response
   
    def make_file(self, response):
          if file_path.exists:
            with open(file_path, 'w') as f:
                 json.dump(response.json(), f)
          else:
            with open(file_path, 'x') as f:
                    json.dump(response.json(), f)

transform()

github = GithubExportService()
config = Config()

res = github.get_commit_request(config.commit_url)
pull = github.get_pull_request(config.pull_url)
github.make_file(res)