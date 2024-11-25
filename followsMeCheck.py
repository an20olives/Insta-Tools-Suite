import instaloader
import getpass
import time
import random
import logging
from instaloader.exceptions import ConnectionException, TwoFactorAuthRequiredException

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create an instance of Instaloader
L = instaloader.Instaloader()

# Prompt for username and password (use getpass to securely input password)
username = input("Enter your Instagram username: ")
password = getpass.getpass("Enter your Instagram password: ")

# Log in to Instagram (this handles basic login)
def login():
    try:
        L.login(username, password)
        print("Login successful!")
    except TwoFactorAuthRequiredException:
        # If 2FA is enabled, prompt for the code
        two_factor_code = input("Enter the 2FA code sent to your device: ")
        L.two_factor_login(two_factor_code)
        print("2FA successful!")

login()

# Fetch the profile of your account
print("Fetching profile...")
profile = instaloader.Profile.from_username(L.context, username)
print("Profile fetched successfully.")

# Function to fetch followers with retry mechanism and rate limit handling
def fetch_followers(profile, max_followers=1000):
    followers = set()
    try:
        for count, follower in enumerate(profile.get_followers()):
            if count >= max_followers:
                break
            followers.add(follower.username)
            if count % 50 == 0:  # After every 50 followers, introduce a pause to avoid rate-limiting
                print(f"Fetched {count} followers...")
                time.sleep(random.uniform(2, 5))  # Randomized sleep to avoid detection by Instagram's anti-bot measures
    except ConnectionException as e:
        print(f"Connection error occurred while fetching followers: {e}")
        time.sleep(10)  # Sleep for 10 seconds and try again
        return fetch_followers(profile, max_followers)
    return followers

# Function to fetch followings with retry mechanism and rate limit handling
def fetch_followings(profile, max_followings=1000):
    followings = set()
    try:
        for count, following in enumerate(profile.get_followees()):
            if count >= max_followings:
                break
            followings.add(following.username)
            if count % 50 == 0:  # After every 50 followings, introduce a pause
                print(f"Fetched {count} followings...")
                time.sleep(random.uniform(2, 5))  # Randomized sleep to avoid detection
    except ConnectionException as e:
        print(f"Connection error occurred while fetching followings: {e}")
        time.sleep(10)  # Sleep for 10 seconds and try again
        return fetch_followings(profile, max_followings)
    return followings

# Fetch followers and followings with retry logic and handling rate limits
followers = fetch_followers(profile)
followings = fetch_followings(profile)

print(f"Found {len(followers)} followers.")
print(f"Found {len(followings)} followings.")

# Save followers and following usernames to files
with open("followers.txt", "w") as f:
    for follower in followers:
        f.write(f"{follower}\n")

with open("followings.txt", "w") as f:
    for following in followings:
        f.write(f"{following}\n")

print("Followers and Followings lists exported successfully.")

# Read the followers and following lists from text files
with open("followers.txt", "r") as f:
    followers = set(f.read().splitlines())

with open("followings.txt", "r") as f:
    followings = set(f.read().splitlines())

# Find who follows you and who doesn't
follows_back = followers.intersection(followings)  # Who follows you back
does_not_follow_back = followings - followers  # Who doesn't follow you back

# Save the results
with open("follows_back.txt", "w") as f:
    for user in follows_back:
        f.write(f"{user}\n")

with open("does_not_follow_back.txt", "w") as f:
    for user in does_not_follow_back:
        f.write(f"{user}\n")

print(f"Users who follow you back saved in 'follows_back.txt'.")
print(f"Users who don't follow you back saved in 'does_not_follow_back.txt'.")
