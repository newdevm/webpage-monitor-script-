import requests
import time
import hashlib
from plyer import notification

# Configuration
URL = "https://www.binance.com/en/support/announcement/new-cryptocurrency-listing?c=48&navId=48&hl=en"  # Replace with the actual webpage URL
CHECK_INTERVAL = 5  # Time between checks in seconds

def get_page_hash(url):
    """
    Fetch the webpage and return its hash value for comparison.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        page_content = response.text
        page_hash = hashlib.sha256(page_content.encode('utf-8')).hexdigest()
        return page_hash
    except requests.RequestException as e:
        print(f"Error fetching webpage: {e}")
        return None

def send_notification(title, message):
    """
    Send a desktop notification.
    """
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=10  # Duration of the notification in seconds
        )
        print("Desktop notification sent successfully!")
    except Exception as e:
        print(f"Failed to send notification: {e}")

def main():
    print(f"Monitoring {URL} for changes...")
    current_hash = get_page_hash(URL)
    if current_hash is None:
        print("Failed to fetch the initial webpage. Exiting...")
        return

    while True:
        time.sleep(CHECK_INTERVAL)  # Wait for the specified interval
        new_hash = get_page_hash(URL)

        if new_hash is None:
            print("Failed to fetch the webpage. Retrying...")
            continue

        if new_hash != current_hash:
            print("Webpage updated!")
            send_notification("Webpage Updated!", f"The webpage at {URL} has been updated.")
            break  # Exit the script or continue monitoring
        else:
            print("No changes detected.")

if __name__ == "__main__":
    main()
