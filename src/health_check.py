#!/usr/bin/env python3

# gia kateythian xrisi se terminal kai oxi hardcoded ston kodika
import argparse
import requests

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check endpoint health and response latency."
    )
    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="Target URL to test ",
    )
    return parser.parse_args()


def check_endpoint(url: str) -> None:
    print(f"Pinging {url}...")
    response = requests.get(url)
    print(f"Response code: {response.status_code}")

    if response.status_code == 200:
        print("Status: ONLINE ")
    else:
        print(f"Status: ERROR (Code {response.status_code})")


if __name__ == "__main__":
    args = parse_arguments()
    check_endpoint(args.url)