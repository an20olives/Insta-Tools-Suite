Instagram Tool Suite - Interface Script

This repository includes a user-friendly interface script (interface.py) for managing Instagram account activities, such as identifying users who don’t follow you back and unfollowing them automatically. It simplifies the process by allowing you to choose tasks through a simple command-line menu.

Features

doesNotFollowChecker9000.py:
Checks which Instagram users don’t follow you back.
Outputs the results to a file (does_not_follow_back.txt).
unfollower.py:
Unfollows users listed in does_not_follow_back.txt.
Includes a confirmation dialog to warn users about temporarily disabling Two-Factor Authentication (2FA/MFA).
Interactive Menu (interface.py):
Allows users to choose between the two scripts (doesNotFollowChecker9000.py or unfollower.py) via a command-line menu.
Includes a 2FA/MFA warning before running the unfollower script to ensure users are aware of required security changes.
Requirements

1. Python Version
Ensure you are using Python 3.7 or later. Python 3.13 is not fully compatible with the instabot library due to imghdr deprecation issues.

2. Required Packages
Install the required dependencies using pip:

pip install -r requirements.txt
The requirements.txt file should include:

instabot==0.117.0
Setup Instructions

Clone the Repository:
Install Dependencies: Run the following command in your terminal:
pip install instabot==0.117.0
Modify instabot Codebase: The instabot library relies on the now-deprecated imghdr library. To resolve this issue, follow these steps:
Locate the api_photo.py file in your Python environment's instabot installation directory:
<your-venv-path>/lib/python3.x/site-packages/instabot/api/api_photo.py
Open the file and comment out the import imghdr line:
# import imghdr
Save the file and restart your script.
Run the Interface Script: Start the interactive menu:
python3 interface.py
Usage Instructions

Start the Tool: Run the interface.py script:
python3 interface.py
Select an Option:

Option 1: Run doesNotFollowChecker9000.py to identify users who don’t follow you back.

Option 2: Run unfollower.py to unfollow users listed in does_not_follow_back.txt.

⚠️ Note: You must temporarily disable Two-Factor Authentication (2FA/MFA) on your Instagram account to use this feature.

Follow Security Prompts:
The script will prompt you to confirm that 2FA is disabled and that you accept the risks before proceeding with unfollowing.
Disclaimer

This tool requires disabling Instagram’s Two-Factor Authentication (2FA/MFA) to perform certain actions via the API.
Use at your own risk, and re-enable 2FA immediately after completing your operations.
Instagram's policies and API usage rules may change over time, which could result in errors or account restrictions. Always ensure compliance with Instagram's terms of service.
