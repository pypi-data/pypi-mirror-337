import argparse
from mocknet_ssh.api import start_mock_server


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--platform", required=True, help="Platform name (e.g., cisco_ios)"
    )
    parser.add_argument("--username", default="admin")
    parser.add_argument("--password", default="admin")
    parser.add_argument("--port", type=int, default=9999)
    args = parser.parse_args()

    start_mock_server(
        platform=args.platform,
        username=args.username,
        password=args.password,
        port=args.port,
    )


if __name__ == "__main__":
    main()
