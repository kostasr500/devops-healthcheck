#!/usr/bin/env python3

# gia kateythian xrisi se terminal kai oxi hardcoded ston kodika
import argparse

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


if __name__ == "__main__":
    args = parse_arguments()
    print(f"Target URL received: {args.url}")