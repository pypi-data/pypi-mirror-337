import os
import json
import time
import datetime
import traceback

def get_credentials():
    """
    Get O*NET API credentials, using cached credentials if they exist and are less than 2 hours old.
    
    Returns:
        tuple: (username, password)
    """
    # Use a fixed path for the cache file
    cache_file = os.path.join(os.path.expanduser("~"), ".onet_credentials.json")
    current_time = time.time()
    cache_duration = 7200  # 2 hours in seconds
    
    # Check if we have cached credentials
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
                
            # Check if credentials are less than 2 hours old
            time_diff = current_time - data['timestamp']
            if time_diff < cache_duration:
                print(f"Using cached credentials (expires in {int((cache_duration-time_diff)/60)} minutes)")
                return data['username'], data['password']
            else:
                print("Cached credentials expired")
        except Exception as e:
            print(f"Error reading cache file: {e}")
    else:
        print("No cache file found")
    
    # Prompt for credentials if no valid cache exists
    print("Please enter your O*NET Web Services credentials:")
    username = input("Username: ")
    password = input("Password: ")
    
    # Save the credentials to cache
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        
        # Write credentials with current timestamp
        with open(cache_file, 'w') as f:
            cache_data = {
                'username': username,
                'password': password,
                'timestamp': current_time
            }
            json.dump(cache_data, f)
            
        # Set appropriate permissions (readable/writable only by the user)
        os.chmod(cache_file, 0o600)
        expiry_time = datetime.datetime.fromtimestamp(current_time + cache_duration)
        print(f"Credentials cached until {expiry_time.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"Warning: Could not save credentials to cache: {str(e)}")
        traceback.print_exc()
    
    return username, password


def get_user_input(prompt):
    result = ''
    while (len(result) == 0):
        result = input(prompt + ': ').strip()
    return result

def check_for_error(service_result):
    if 'error' in service_result:
        # print(f"Error: {service_result['error']}")
        return True
    return False