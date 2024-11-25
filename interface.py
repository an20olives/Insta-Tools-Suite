import os
import subprocess

def main():
    print("Welcome to the Instagram Tool Suite!")
    print("Please select an option:")
    print("1. Run 'followsMeCheck.py' to check who doesn't follow you back")
    print("2. Run 'unfollowerScript.py' to unfollow users listed in 'does_not_follow_back.txt'")
    print("3. Exit")

    while True:
        try:
            choice = int(input("Enter your choice (1/2/3): "))
            if choice == 1:
                print("Running 'followsMeCheck.py'...")
                run_script("followsMeCheck.py")
                break
            elif choice == 2:
                print_warning_and_confirm()
                break
            elif choice == 3:
                print("Exiting the tool. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number (1/2/3).")

def print_warning_and_confirm():
    """
    Warns the user about disabling MFA/2FA and asks for explicit confirmation.
    """
    print("\nIMPORTANT NOTICE:")
    print("This tool requires that you disable Two-Factor Authentication (2FA/MFA) on your Instagram account.")
    print("Please disable MFA temporarily and understand the risks involved.")
    print("You can re-enable MFA/2FA immediately after this operation is completed.")
    print("\nTo proceed, type 'YES' to confirm that you have disabled MFA/2FA and understand the risks.")
    print("Otherwise, type anything else to return to the main menu.")

    confirmation = input("Enter your confirmation: ")
    if confirmation.strip().upper() == "YES":
        print("Confirmation received. Running 'unfollowerScript.py'...")
        run_script("unfollowerScript.py")
    else:
        print("Operation canceled. Returning to the main menu.")

def run_script(script_name):
    """
    Runs a Python script located in the same directory as this script.
    """
    try:
        # Using subprocess to execute the selected script
        subprocess.run(["python3", script_name], check=True)
    except FileNotFoundError:
        print(f"Error: '{script_name}' not found. Please ensure the file is in the same directory as 'interface.py'.")
    except subprocess.CalledProcessError as e:
        print(f"Error: There was an issue running '{script_name}'.\n{e}")

if __name__ == "__main__":
    main()
