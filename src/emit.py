import argparse
import boto3
import json
from datetime import datetime

session = boto3.session.Session()
client = session.client("events")
bus = "slack-destination"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", required=True, help="slack channel")
    ap.add_argument("--text", required=True, help="message to send to the channel")
    args = ap.parse_args()
    payload = {
        "channel": args.channel,
        "text": args.text
    }
    response = client.put_events(
        Entries=[
            {
                "EventBusName": bus,
                "Source": "cloud.heeki.emit",
                "Time": datetime.now(),
                "DetailType": "custom",
                "Detail": json.dumps(payload)
            }
        ]
    )
    print(json.dumps(response))

if __name__ == "__main__":
    main()
