# pyutils_lib

The pyutils_lib is a python library that establishes a coding framework and provides common functionalities to be used by python applications.

The current features are... 
- Configuration Management
- Logging
- Reporting

## Configuration Requirements
 - Install Python
 - Install PIPEnv

## Setup Instructions for referencing iti_pyutils_lib
- Checkout this repo to the same parent folder as your project
- Edit the Pipfile in your repo to include the reference to pyutils_lib folder
	- `pyutils_lib = {path = "./../pyutils_lib",editable = true}`
- Execute "pipenv install --dev" from the command line in the your project folder
