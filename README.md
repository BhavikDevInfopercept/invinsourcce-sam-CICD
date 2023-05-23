# Invinsource-Backend
<hr>
A brief description of what this project does and who it's



## Architecture Diagram
<hr>
![MicrosoftTeams-image (2)](https://github.com/Sandiptank70/lambda/assets/53286381/519f5859-7749-4f95-81a0-05be4ec3b20a)


## API Gateway
<hr>

    |------API
    |       |--AdminToUSer
    |       |--AdminUSerGlobalSignout
    |       |--AllUserProfile
    |       |--UpdateProfileAdmin
    |       |--DisableUserstatus
    |       |--EnableUser
    |       |--UpdateProfileAdmin
    |       |--UserToAdmin
    | ----  |--Auth
    |          |--Conform Password
    |          |--Forgot
    |          |--Conform Password
    |          |--Login
    |          |--Register
    |-----|--User
                |--UserConformSignup
                |--UploadImage
                |--GetProfile
                |--UpdateProfileUser

 

## Prerequisites
<hr>

python 3.8

AWS CLI


## installation
<hr>

* AWS CLI (Command Line Interface) is a unified tool that allows you to interact with various AWS services through the command line. This guide will walk you through the installation process for AWS CLI on your system.


### Python3.8
<hr>

```bash
[https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://www.python.org/downloads/release/python-380/)
```


### AWS CLI
<hr>

```bash
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
```
## Configuring the AWS CLI
<hr>

1. Open a terminal or command prompt.
2. Run the following command to start the configuration process:
   ```bash
   aws configure
   ```
Note : Provide Your "AWS Access Key ID" And "AWS Secret Access Key"


## Deployment Steps
<hr>

Clone this project onto your hard drive:
```bash
  gh repo clone Infopercept/invinsource
```
* make repository at root directory named ".github"
* inside ".github" directory make directory called "workflows"


### Creating the sam-pipeline.yml file
<hr>

* GitHub CI/CD pipelines are configured using a YAML file. This file configures what specific action triggers a workflow, such as push on main, and what workflow steps are required.
* In the root of the repository containing the files generated by sam init, create the directory: `.github/workflows`.
* ![MicrosoftTeams-image (3)](https://github.com/Sandiptank70/lambda/assets/53286381/cbeab655-23b1-4877-8e24-6cd872c7a878)

 

### Edit the sem-pipeline.yaml
<hr>

```bash
on:
    push:
      branches:
        - main
jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - uses: aws-actions/setup-sam@v1
      - uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.REGION }}

      # sam validate
      - run: sam validate --lint
      # sam build 
      - run: sam build
      # Run Unit tests- Specify unit tests here 
      # sam deploy
      - run: sam deploy --capabilities CAPABILITY_NAMED_IAM --no-confirm-changeset --no-fail-on-empty-changeset --stack-name sam-hello-world --region ##region##
```
* Replace ##region## with your AWS Region.

The configuration triggers the GitHub Actions CI/CD pipeline when code is pushed to the main branch. You can amend this if you are using another branch.


## Configuring AWS credentials in GitHub
<hr>

The GitHub Actions CI/CD pipeline requires AWS credentials to access your AWS account. The credentials must include AWS Identity and Access Management (IAM) policies that provide access to Lambda, API Gateway, AWS CloudFormation, S3, and IAM resources.

has context menu


These credentials are stored as GitHub secrets within your GitHub repository, under Settings > Secrets.

In your GitHub repository, create two secrets named AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and enter the key values. We recommend following IAM best practices for the AWS credentials used in GitHub Actions workflows, including:

* Do not store credentials in your repository code. Use GitHub Actions secrets to store credentials and redact credentials from GitHub Actions workflow logs.
* Create an individual IAM user with an access key for use in GitHub Actions workflows, preferably one per repository. Do not use the AWS account root user access key.
* Grant least privilege to the credentials used in GitHub Actions workflows. Grant only the permissions required to perform the actions in your GitHub Actions workflows.
* Rotate the credentials used in GitHub Actions workflows regularly.
* Monitor the activity of the credentials used in GitHub Actions workflows.

 

## Deploy Application
<hr>

```bash
git add .

git commit -am "Add AWS SAM files" 

git push

```
Once the files are pushed to GitHub on the main branch, this automatically triggers the GitHub Actions CI/CD pipeline as configured in the sam-pipeline.yml file.

The GitHub actions runner performs the pipeline steps specified in the file. It checks out the code from your repo, sets up Python, and configures the AWS credentials based on the GitHub secrets. The runner uses the GitHub action setup-sam to install AWS SAM CLI.

The pipeline triggers the sam build process to build the application artifacts, using the default container image for Python 3.8.

sam deploy runs to configure the resources in your AWS account using the securely stored credentials.

To view the application deployment progress, select Actions in the repository menu. Select the workflow run and select the job name build-deploy.

If the build fails, you can view the error message. Common errors are:
  * Incompatible software versions such as the Python runtime being different from the Python version on the build machine. Resolve this by installing the proper software versions.
  * Credentials could not be loaded. Verify that AWS credentials are stored in GitHub secrets.
  * Ensure that your AWS account has the necessary permissions to deploy the resources in the AWS SAM template, in addition to the S3 deployment bucket.

 

## Testing the application
<hr>

* Within the workflow run, expand the Run sam deploy section.
* Navigate to the AWS SAM Outputs section. The HelloWorldAPI value shows the API Gateway endpoint URL deployed in your AWS account.
* Use curl to test the API:
 ```bash
curl https://<api-id>.execute-api.us-east-1.amazonaws.com/Prod/hello/
```

## Cleanup
<hr>

To remove the application resources, navigate to the CloudFormation console and delete the stack. Alternatively, you can use an AWS CLI command to remove the stack:
```bash
aws cloudformation delete-stack --stack-name sam-hello-world
```

 


## License
<hr>

[MIT](https://choosealicense.com/licenses/mit/)

 

## :computer: Website
<hr>

[https://infopercept.com](https://infopercept.com)

 

## :raised_hands: Support
<hr>

* [Email](mailto:sos@infopercept.com)
* [Open issue](https://github.com/Infopercept/compromise-assessment/issues)
* [Infopercept.com](https://infopercept.com/contact)

 
## :family: Contributors
<hr>

<table> 
    <tr>
        <td align="center"><a href="https://github.com/PrajapatiBhavik"><img src="https://avatars.githubusercontent.com/u/67953602?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Bhavik Prajapati</b></sub></a><br /><a href="https://github.com/PrajapatiBhavik" title="Code">:computer:</a></td>
        <td align="center"><a href="https://github.com/Sandiptank70"><img src="https://avatars.githubusercontent.com/u/67953602?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Sandip Tank</b></sub></a><br /><a href="https://github.com/PrajapatiBhavik" title="Code">:computer:</a></td>
    </tr>
</table>