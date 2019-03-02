import github_io

REPO_TO_CLONE = 'Eric-Melb/self-cloner'

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
                print('Code: {}'.format(access_code))
        except KeyError:
                response = api_response
                response['statusCode'] = 400
                response['body'] = 'OAuth Authentication or Redirect Failure'

                return response

        # exchange code for an access token
        token = github_io.code_for_token(access_code)

        # use token to clone repo into users account
        response = github_io.clone_public_repo(token, REPO_TO_CLONE)

        return api_response


