#!/usr/bin/env python3

# gia kateythian xrisi se terminal kai oxi hardcoded ston kodika
import argparse
import requests
import time

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

    # latency counter start
    start_time = time.perf_counter()

    response = requests.get(url)

    # stop counter 
    elapsed_ms = round( (time.perf_counter() - start_time) * 1000, 2 )

    if response.status_code == 200:
        print(f"Status: ONLINE | Latency: {elapsed_ms}ms | Code: {response.status_code}")
    else:
        print(f"Status: ERROR | Latency: {elapsed_ms}ms | Code: {response.status_code}")



if __name__ == "__main__":
    args = parse_arguments()
    check_endpoint(args.url)