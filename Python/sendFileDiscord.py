import argparse
import requests

def send_file_to_discord(webhook_url, file_path, username="File Bot", content=""):
    with open(file_path, "rb") as file:
        files = {"file": (file_path, file)}
        data = {"username": username, "content": content}
        response = requests.post(webhook_url, files=files, data=data)

        if response.status_code == 200:
            print(f"File '{file_path}' successfully sent to Discord.")
        else:
            print(f"Failed to send file to Discord. Status code: {response.status_code}")

def main():
    parser = argparse.ArgumentParser(description="Send a file to Discord using a webhook.")
    parser.add_argument("-f", "--file", required=True, help="Path to the file you want to send.")
    parser.add_argument("-wh", "--webhook", required=True, help="Discord webhook URL.")
    parser.add_argument("-u", "--username", default="File Bot", help="Username for the bot.")
    parser.add_argument("-c", "--content", default="", help="Additional text content to be sent along with the file.")
    args = parser.parse_args()

    send_file_to_discord(args.webhook, args.file, username=args.username, content=args.content)

if __name__ == "__main__":
    main()