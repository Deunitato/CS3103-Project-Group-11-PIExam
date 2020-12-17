# Online E-Examination Program

This program is meant as a easy E-examination program that project questions in CLI for students as well as logging the ports used during the time. Note that this program meant to be used on a raspberry pi 

(This program will create a virtual environment)

## Dependencies
- Python3
- Allowed virtual env
- Raspberry pi
- Gmail account with "less secure application" allowed in security

## Configuration

Configerables includes:
- Name of the reciever
- email address of reciever
- Question list
- Duration of the netstat log

Path: `/config`

## Running
- Ensure you are in the main folder
- `bash ./run.sh`

## Output
- Output is stored in the Data folder
- Output is emailed to recipient stated in the config folder
