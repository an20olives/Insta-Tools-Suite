import os
import time
import random
import getpass
from instabot import Bot
from typing import List, Set
from datetime import datetime, timedelta


class InstagramUnfollower:
    def __init__(self):
        self.bot = None
        self.whitelist = set()
        self.users_to_unfollow = set()
        self.unfollows_today = 0
        self.last_unfollow_time = None

        # Rate limiting constants
        self.MAX_UNFOLLOWS_PER_DAY = 900
        self.MAX_UNFOLLOWS_PER_HOUR = 150
        self.MIN_DELAY = 5  # minimum seconds between unfollows
        self.MAX_DELAY = 15  # maximum seconds between unfollows

    def load_whitelist(self, whitelist_path: str) -> None:
        """Load whitelist users from file."""
        try:
            with open(whitelist_path, 'r') as f:
                self.whitelist = {line.strip() for line in f if line.strip()}
            print(f"Loaded {len(self.whitelist)} users from whitelist")
        except FileNotFoundError:
            print(f"Warning: Whitelist file {whitelist_path} not found")
            self.whitelist = set()

    def load_unfollow_list(self, unfollow_path: str) -> None:
        """Load users to unfollow from file."""
        try:
            with open(unfollow_path, 'r') as f:
                self.users_to_unfollow = {line.strip() for line in f if line.strip()}
            print(f"Loaded {len(self.users_to_unfollow)} users to unfollow")
        except FileNotFoundError:
            print(f"Error: Required file {unfollow_path} not found")
            exit(1)

    def clean_previous_session(self):
        """Clean up cookies and session files from previous runs."""
        cookie_pattern = "config/*.cookie"
        session_pattern = "config/*_uuid_and_cookie.json"

        try:
            # Create config directory if it doesn't exist
            os.makedirs('config', exist_ok=True)

            # Remove existing cookie files
            os.system(f"rm -f {cookie_pattern}")
            os.system(f"rm -f {session_pattern}")
            print("Cleaned previous session files")
        except Exception as e:
            print(f"Warning: Could not clean previous session files: {str(e)}")

    def authenticate(self) -> bool:
        """Handle authentication with username and password."""
        try:
            # Clean previous session files
            self.clean_previous_session()

            username = input("Enter your Instagram username: ")
            password = getpass.getpass("Enter your Instagram password: ")

            # Initialize bot with minimal settings
            self.bot = Bot(
                max_likes_per_day=0,
                max_follows_per_day=0,
                max_unfollows_per_day=self.MAX_UNFOLLOWS_PER_DAY,
                unfollow_delay=self.MIN_DELAY
            )

            # Set up additional bot settings
            self.bot.proxy = None
            self.bot.skip_pending_requests = True

            # Attempt login
            print("\nAttempting to log in... This might take a moment...")
            login_success = self.bot.login(
                username=username,
                password=password,
                use_cookie=False
            )

            if login_success:
                print("Successfully logged in!")
                return True
            else:
                print("Login failed. Please check your credentials.")
                return False

        except Exception as e:
            print(f"Authentication failed: {str(e)}")
            return False

    def security_check(self) -> bool:
        """Perform security verification before unfollowing."""
        print("\n=== SECURITY VERIFICATION ===")
        print(f"Total users to unfollow: {len(self.users_to_unfollow - self.whitelist)}")
        print("\nRate Limiting Information:")
        print(f"- Maximum {self.MAX_UNFOLLOWS_PER_DAY} unfollows per day")
        print(f"- Maximum {self.MAX_UNFOLLOWS_PER_HOUR} unfollows per hour")
        print(f"- Random delay of {self.MIN_DELAY}-{self.MAX_DELAY} seconds between actions")
        print("\nThis action will unfollow users who don't follow you back (excluding whitelisted users)")

        verification = input("\nType 'DELETE' to confirm unfollowing these users: ")
        return verification.strip().upper() == "DELETE"

    def should_continue(self) -> bool:
        """Check if we should continue unfollowing based on rate limits."""
        current_time = datetime.now()

        # First action
        if not self.last_unfollow_time:
            self.last_unfollow_time = current_time
            return True

        # Check daily limit
        if self.unfollows_today >= self.MAX_UNFOLLOWS_PER_DAY:
            print("\nReached daily unfollow limit. Please try again tomorrow.")
            return False

        # Check hourly limit
        hour_ago = current_time - timedelta(hours=1)
        if (self.unfollows_today % self.MAX_UNFOLLOWS_PER_HOUR) == 0 and \
                self.last_unfollow_time > hour_ago:
            wait_seconds = 3600 - (current_time - self.last_unfollow_time).seconds
            print(f"\nReaching hourly limit. Pausing for {wait_seconds // 60} minutes...")
            time.sleep(wait_seconds)

        return True

    def verify_user_exists(self, username: str) -> bool:
        """Verify if a user exists before attempting to unfollow."""
        try:
            user_id = self.bot.get_user_id_from_username(username)
            return user_id is not None
        except:
            return False

    def unfollow_users(self) -> None:
        """Unfollow users with rate limiting and progress tracking."""
        users_to_process = self.users_to_unfollow - self.whitelist
        total_users = len(users_to_process)

        print(f"\nStarting unfollow process for {total_users} users")

        for idx, username in enumerate(users_to_process, 1):
            try:
                if not self.should_continue():
                    break

                print(f"\n[{idx}/{total_users}] Processing: {username}")
                print(f"Unfollows today: {self.unfollows_today}/{self.MAX_UNFOLLOWS_PER_DAY}")

                # Verify user exists before attempting to unfollow
                if not self.verify_user_exists(username):
                    print(f"Skipping {username} - User not found")
                    continue

                if self.bot.unfollow(username):
                    print(f"Successfully unfollowed: {username}")
                    self.unfollows_today += 1
                    self.last_unfollow_time = datetime.now()
                else:
                    print(f"Failed to unfollow: {username}")

                # Random delay between actions
                delay = random.uniform(self.MIN_DELAY, self.MAX_DELAY)
                print(f"Waiting {delay:.1f} seconds before next action...")
                time.sleep(delay)

            except Exception as e:
                print(f"Error unfollowing {username}: {str(e)}")
                continue

        print("\nUnfollow session completed!")
        print(f"Total unfollows this session: {self.unfollows_today}")


def main():
    unfollower = InstagramUnfollower()

    # Load required files
    print("\n=== Loading Required Files ===")
    unfollower.load_whitelist("whitelist.txt")
    unfollower.load_unfollow_list("does_not_follow_back.txt")

    # Authenticate
    print("\n=== Authentication ===")
    if not unfollower.authenticate():
        print("Authentication failed. Please try again.")
        return

    # Security check
    if not unfollower.security_check():
        print("Operation cancelled by user")
        return

    # Execute unfollow process
    print("\n=== Starting Unfollow Process ===")
    unfollower.unfollow_users()

    print("\n=== Process Complete ===")
    print("Remember to check your Instagram activity log for verification")


if __name__ == "__main__":
    main()