## EventBridge and Slack sample
Below is an example repository for configuring EventBridge API destinations to Slack.

## Slack application setup
1. Navigate to https://api.slack.com/apps
2. Click on "Create New App"
3. Click on "From scratch"
4. Input "App Name" and select the workspace where the application will be used
5. Under Basic Information, Install your app, click the "Install to Workspace" button
6. Click "Allow"
7. Under Features, select "OAuth & Permissions"
8. Under OAuth Tokens, copy the "Bot User OAuth Token" for later
9. Under Scopes, add "chat:write" permissions in the "Bot Token Scopes" section

## Slack channel setup:
1. Create a public channel in which the bot will post messages
2. Add the application to the public channel

## Secrets Manager setup
1. Navigate to https://console.aws.amazon.com/secretsmanager/
2. Click on "Store a new secret"
3. Click on "Other type of secrets"
4. Select "Plaintext"
5. Enter the following text: "Bearer xoxb-[your_bot_user_oauth_token]"
6. Click "Next"
7. Enter the "Secret name", which is what you'll reference later as a CloudFormation parameter

## CloudFormation
Define the template parameters:
* pName: name of the custom EventBridge bus, e.g. slack-destination
* pEndpoint: Slack endpoint, e.g. https://slack.com/api/chat.postMessage
* pSecretId: the name of the Secrets Manager you stored above, e.g. /slack/eventbridge
* pLambdaArn: (optional) additional function target for troubleshooting events

Deploy the stack.
Note: In this example, the channel name was assumed to be "aws-integration-testing" and is reflected in the event pattern.
Note: An optional Lambda template was included for testing incoming events and is not required for the solution.

## Testing
Execute the provided test script:

```bash
python3 src/emit.py --channel aws-integration-testing --text "hello world" | jq
```

## Environment
For simplicity of deployment, a `makefile` is provided. However, it requires an environment file (`/etc/environment.sh`) to be configured as follows:

```bash
S3BUCKET=your-bucket
PROFILE=your-aws-cli-profile

P_NAME=slack-destination
P_ENDPOINT=https://slack.com/api/chat.postMessage
P_SECRETID=your-secret-id

EVENTBRIDGE_STACK=slack-eventbridge
EVENTBRIDGE_TEMPLATE=iac/eventbridge.yaml
EVENTBRIDGE_OUTPUT=iac/eventbridge_output.yaml
EVENTBRIDGE_PARAMS="ParameterKey=pName,ParameterValue=${P_NAME} ParameterKey=pEndpoint,ParameterValue=${P_ENDPOINT} ParameterKey=pSecretId,ParameterValue=${P_SECRETID}"

# O_EVENTBRIDGE_RULE=your-eventbridge-rule-arn
# P_FN_MEMORY=128
# P_FN_TIMEOUT=15

# LAMBDA_STACK=slack-lambda
# LAMBDA_TEMPLATE=iac/lambda.yaml
# LAMBDA_OUTPUT=iac/lambda_output.yaml
# LAMBDA_PARAMS="ParameterKey=pFnMemory,ParameterValue=${P_FN_MEMORY} ParameterKey=pFnTimeout,ParameterValue=${P_FN_TIMEOUT} ParameterKey=pRuleArn,ParameterValue=${O_EVENTBRIDGE_RULE}"
```