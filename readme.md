# self-forker

Clicking this URL will fork this repo into your github.: https://github.com/login/oauth/authorize?scope=public_repo&client_id=d6c4f41e597356bfef63

## Deployment 

### Notes
To aid deployment onto AWS Lambda a `lambda_package.zip` file is provided. As well as the two Python source files specific to this project (`lambda_function.py` and `github_io.py`) this archive contains the Python `requests` library and its dependencies. This packaging is necessary for running on the AWS Lambda platform.

### Quick Deployment Overview
##### AWS
Create a Lambda with a default IAM role and upload lambda_package.zip
    
Setup an API Gateway for a REST API with a single Lambda proxy resource, select the Lambda you just created, deploy the gateway

##### Github
Register an OAuth App from the developer menu, using your API gateway's invocation URL as the homepage and the same URL plus "/callback" as the callback.

Go back to AWS and put the Client ID and Client Secret in the Lambda environment variables as `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` respectively. Change the `REPO_TO_FORK` variable in `lambda_function.py` if you want to a fork a different repo.

The URL to activate (fork the repo) is `https://github.com/login/oauth/authorize?scope=public_repo&client_id=[]` where `[]` is your Client ID.  

### Detailed Deployment Steps

##### Configuring AWS

1. In AWS select the Amazon API Gateway product
2. Click Get Started
3. Select New API
4. Select REST as the protocol
5. Provide any API name and an endpoint type of Regional
6. Click create API
7. Click the Actions button and select Create Resource
8. Click the "Configure as proxy resource" checkbox
9. Click the "Create Resource" button
10. With the integration type "Lambda Function Proxy" selected a link to create a Lambda Function should appear. If the link has not appeared, simply navigate to the Lambda product in AWS and create a new Lambda.
11. In Create Lambda, select "Author from scratch"
12. Type in any name, I've used "selfforker"
13. Select Python 3.7 as the runtime
14. Select Create a Custom IAM Role
15. There is no need to modify the policy document, name the lambda as you please
16. Click Allow
17. In the Lambda editor for this Lambda, go down to the "Function Code" section and find the "Code entry type" dropdown. Select "Upload a .zip file" from the dropdown menu.
18. Click on the Upload button
19. From this repo, select the `lambda_package.zip` file
20. At the top of the window, hit Save
21. Return to the API gateway interface for our API and select the proxy resource
22. When selected it should say "Method not set up. Set up now." Click on "Set up now."
23. Type in the name of the Lambda, I used "selfforker"
24. In the add permission dialogue, click "Ok"
25. Click on Actions and select "Deploy API"
26. Choose a Stage name (such as "live") and a Stage description (such as "live usage")
27. Click the Deploy button
28. The invoke URL (at the top of the page) will be needed for the github OAuth setup

##### Configuring Github

1. Register a new OAuth application via Settings -> Developer Settings -> New OAuth App
2. For the Homepage URL, use the API Gateway Invocation URL
3. For the callback URL, use the Invocation URL plus "/callback"
4. Put the client ID and Secret into your environment variables back in the lambda configuration, named GITHUB_CLIENT_ID & GITHUB_CLIENT_SECRET respectively

The URL to activate (fork the repo) is `https://github.com/login/oauth/authorize?scope=public_repo&client_id=[]` where `[]` is your Client ID.

## Technical Notes
This program is a very small (sub 100 lines) self-forking repo. 
It negotiates the Github API OAuth flow asking for `public_repo` access using the link provided by Github, then calls the API Gateway with the provided access code, triggering the Lambda. The Lambda validates that it was triggered with a code, then uses the requests library to exchange the code for a token, and then uses the token to fork the repo.  

Print statements go to the lambda's Cloudwatch logs, you can access these from the Lambda setup by clicking on Monitoring -> View Logs in Cloudwatch.
