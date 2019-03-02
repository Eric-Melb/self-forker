import requests
import json
import os

REPOS_ENDPOINT = 'https://api.github.com/repos'
TOKEN_EXCHANGE = 'https://github.com/login/oauth/access_token'


# exchange an access code for an access token
def code_for_token(access_code):
        cid = os.environ['GITHUB_CLIENT_ID']
        secret = os.environ['GITHUB_CLIENT_SECRET']

        url = TOKEN_EXCHANGE

        url_params = {
                'client_id': cid,
                'client_secret': secret,
                'code': access_code
        }

        head = {'Accept': 'application/json'}

        response = requests.post(
                url,
                params=url_params,
                headers=head
        )

        token = json.loads(response.content)["access_token"]

        return token


# forks the specified repo into the token bearer's account
# returns True/False for Success/Failure
def fork_public_repo(token, repo):
        head = {'Authorization': 'token {}'.format(token)}
        url = REPOS_ENDPOINT + '/' + repo + '/' + 'forks'

        print("URL: {}".format(url))

        response = requests.post(url, headers=head)

        if response.status_code == 202:
                return True
        else:
                # log failure
                print("Error: {}".format(response.text))
                return False

