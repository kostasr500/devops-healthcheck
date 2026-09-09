#!/usr/bin/env python3

# gia kateythian xrisi se terminal kai oxi hardcoded ston kodika
import argparse
import requests
import time
import sys
import json

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
    # error for timeout vale meta tin entoli an thes alli timi
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Request timeout",
    )
    # an to epilexeis stin entoli allios einai off
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format",
    )

    return parser.parse_args()


def check_endpoint(url: str, timeout: float, as_json: bool) -> None:
    start_time = time.perf_counter()

    try:
        response = requests.get(url, timeout=timeout)
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        is_healthy = 200 <= response.status_code < 300

        result = {
            "status": "ONLINE" if is_healthy else "ERROR",
            "url": url,
            "status_code": response.status_code,
            "latency_ms": elapsed_ms,
            "error": None,
        }

        if as_json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Status: {result['status']} | Latency: {elapsed_ms}ms | Code: {response.status_code}")

        sys.exit(0 if is_healthy else 1)

    except requests.exceptions.Timeout:
        result = {
            "status": "TIMEOUT",
            "url": url,
            "status_code": None,
            "latency_ms": None,
            "error": f"Exceeded timeout limit of {timeout}s",
        }
        if as_json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Status: TIMEOUT | {result['error']}")
        sys.exit(2)

    except requests.exceptions.RequestException as err:
        result = {
            "status": "CONNECTION ERROR",
            "url": url,
            "status_code": None,
            "latency_ms": None,
            "error": str(err),
        }
        if as_json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Status: CONNECTION ERROR | {err.__class__.__name__}")
        sys.exit(2)


if __name__ == "__main__":
    args = parse_arguments()
    check_endpoint(args.url, args.timeout, args.json)