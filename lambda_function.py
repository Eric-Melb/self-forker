import github_io

REPO_TO_FORK = 'Eric-Melb/self-forker'

# lambda + api gateway valid response template
api_response = {
                'statusCode': 200,
                'headers': {'content-type': 'application/json'},
                'body': 'hi'
}


# ENTRY POINT
# receive lambda event
def lambda_handler(event, context):

        # check this is a valid OAuth redirect
        try:
                access_code = event['queryStringParameters']['code']
        except KeyError:
                response = api_response
                response['statusCode'] = 400
                response['body'] = 'OAuth Authentication or Redirect Failure'

                return response

        # exchange code for an access token
        token = github_io.code_for_token(access_code)

        # use token to clone repo into users account
        success = github_io.fork_public_repo(token, REPO_TO_FORK)

        if success:
                response = api_response
                response['statusCode'] = 200
                response['body'] = 'Repository successfully forked'

                return response
        else:
                response = api_response
                response['statusCode'] = 500
                response['body'] = 'Unable to fork repository'

                return response
