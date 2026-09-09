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
        help="Target URL to test",
    )
    # error for timeout 
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Request timeout",
    )
    return parser.parse_args()


def check_endpoint(url: str, timeout: float) -> None:
    print(f"Pinging {url} (timeout: {timeout}s)...")
    start_time = time.perf_counter()

    try:
        response = requests.get(url, timeout=timeout)
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

        if 200 <= response.status_code < 300:
            print(f"Status: ONLINE | Latency: {elapsed_ms}ms | Code: {response.status_code}")
        else:
            print(f"Status: ERROR | Latency: {elapsed_ms}ms | Code: {response.status_code}")

    except requests.exceptions.Timeout:
        print(f"Status: TIMEOUT | Failed to respond within {timeout}s")
    except requests.exceptions.RequestException as err:
        print(f"Status: CONNECTION ERROR | Could not reach host ({err.__class__.__name__})")


if __name__ == "__main__":
    args = parse_arguments()
    check_endpoint(args.url, args.timeout)