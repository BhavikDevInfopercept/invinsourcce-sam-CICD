<div>
  <h1 align="center">Invinsource Backend</h1>
  <br>
  <img align="left" alt="Invinsense logo" src="https://github.com/BhavikDevInfopercept/Compromise-Assesment-Python-Script/blob/master/templates/Invinsense_logo_tagline.svg" width="300px">
  <img align="right" alt="Infopercept logo" src="https://github.com/BhavikDevInfopercept/Compromise-Assesment-Python-Script/blob/master/templates/Infopercept_logo%202.svg" width="300px">
  <br>
</div>
<br>
<br>


## :orange_book: About the Invinsource Backend
AWS Compromise Assessment compiles the events and Indicator of Compromise (IoC) from CloudTrail Logs after an incident has occurred or appears to be compromised. It will assist in obtaining complete critical event data and making it easier for threat hunters for future forensics.



## :book: Architecture Diagram 
<div>
    </br>
    <img align="left" alt="Invinsource Backend Architechture Diagram" src="C:\Users\bhavikp\OneDrive\Desktop\AWS-Cognito.drawio.png"/>
    </br>
</div>


## :high_brightness: Project Structure
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   ├── com/
│   │   │   │   ├── example/
│   │   │   │   │   ├── controllers/
│   │   │   │   │   ├── models/
│   │   │   │   │   └── utils/
│   │   ├── resources/
│   │   │   ├── config/
│   │   │   ├── static/
│   │   │   └── templates/
│   └── test/
│       └── java/
│           └── com/
│               └── example/
│


## :white_check_mark: How to run the script

### :inbox_tray: Installation of python
Python for Windows
    
```bash
https://www.digitalocean.com/community/tutorials/install-python-windows-10
```
Python for Ubuntu/Linux
    
```bash
https://www.makeuseof.com/install-python-ubuntu/
```

### :nut_and_bolt: Configuration of AWS SDK
Install AWS CLI from the link given below
    
```bash 
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
```

Run the following command and provide your aws credentials to setup the AWS ADK on your system.

```bash
aws configure
```

### :syringe: Install required python dependency
Open the command prompt or terminal on your system then reach to project directory and run the following command

```bash
pip3 install -r requirements.txt
```
   
### :open_file_folder: Clone the GitHub repository
```bash
https://github.com/Infopercept/compromise-assessment
```

### :newspaper: Note
> If you are `Windows` user then use `python` for running the script.

or

> If you are `Ubunt/Linux/MacOs` user then use `python3` for runnig the script.

### :bulb: Help for script command
Type the following command

```bash
python3 compromise-assessment.py -h
```
or
```bash
python3 compromise-assessment.py --help
```
Result

<img alt="help-ss" src="https://github.com/BhavikDevInfopercept/Compromise-Assesment-Python-Script/blob/master/templates/compromise-assessment-help-ss.png">

### :arrow_forward: Run the compromise assessment script
- You can use this arguments to make user specific choices and arguments optionals are `days`, `record_limit`, and `service_name`.
- Commands you can use:

| Command                                                                           | Description                                                                                                                                            |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| python3 compromise-assessment.py                                                  | This command gives you the 90 days cloudtrail records as default it takes 90 days,it will take all services and it will return 5000 record by default. |
| python3 compromise-assessment.py -days 60                                         | This command gives you the 60 days cloudtrail records, it will take all services and it will return 5000 record by default.                            |
| python3 compromise-assessment.py -days 90                                         | This command gives you the 90 days cloudtrail records, it will take all services and it will return 5000 record by default.                            |
| python3 compromise-assessment.py -record_limit 1000                               | This command gives you the 90 days cloudtrail records as default, it will take all services and it will return 1000 record.                            |
| python3 compromise-assessment.py -service_name s3                                 | This command gives you the 90 days cloudtrail records as default, it will take S3 services and it will return 5000 record.                             |
| python3 compromise-assessment.py -days 60 -service_name iam                       | This command gives you the 60 days cloudtrail records, it will take IAM services and it will return 5000 record.                                       |
| python3 compromise-assessment.py -days 70 -record_limit 5000 -service_name lambda | This command gives you the 70 days cloudtrail records, it will take LAMBDA services and it will return 5000 record.                                    |
| python3 compromise-assessment.py -service_name lambda                             | This command gives you the 90 days cloudtrail records, it will take LAMBDA services and it will return 5000 record.                                    |
| python3 compromise-assessment.py -service_name s3 lambda                          | This command gives you the 90 days cloudtrail records, it will take LAMBDA and S3 services and it will return 5000 record.                             |
| python3 compromise-assessment.py -service_name lambda iam                         | This command gives you the 90 days cloudtrail records, it will take LAMBDA and IAM services and it will return 5000 record.                            |
| python3 compromise-assessment.py -service_name lambda iam s3                      | This command gives you the 90 days cloudtrail records, it will take S3, LAMBDA, and, IAM services and it will return 5000 record.                      |


## :cinema: Repository Visualization
<div align="center">
    <img alt="Report" src="https://github.com/BhavikDevInfopercept/Compromise-Assesment-Python-Script/blob/master/templates/report-ss.png" /><br>
    <img alt="Report" src="https://github.com/BhavikDevInfopercept/Compromise-Assesment-Python-Script/blob/master/templates/report-ss-2.png" />
</div>


## :key: License
Licensed under the (https://www.infopercept.com/) License, Version 3.0.
Copyright 2022 Infopercept. [Copy of the license](LICENSE).


## :computer: Website
[https://infopercept.com](https://infopercept.com)


## :raised_hands: Support
* [Email](mailto:sos@infopercept.com)
* [Open issue](https://github.com/Infopercept/compromise-assessment/issues)
* [Infopercept.com](https://infopercept.com/contact)


## :family: Contributors 

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>  
  <tr>
    <td align="center"><a href="https://github.com/PrajapatiBhavik"><img src="https://avatars.githubusercontent.com/u/67953602?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Bhavik Prajapati</b></sub></a><br /><a href="https://github.com/PrajapatiBhavik" title="Code">:computer:</a></td>
  </tr>
</table>

## Author

👤 **Bhavik Prajapati**

- Twitter: [@_BhavikP_55_](https://twitter.com/_BhavikP_55_)
- Github: [@PrajapatiBhavik](https://github.com/PrajapatiBhavik)
