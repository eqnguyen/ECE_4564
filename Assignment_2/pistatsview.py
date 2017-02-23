#! /usr/bin/env python3

import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', required=True, help='IP/named address of the message broker')
    parser.add_argument('-p', type=int, help='Virtual host (defaualt is "/")')
    parser.add_argument('-c', type=int, help='login:password')
    parser.add_argument('-k', type=int, required=True, help='routing key')

    args = parser.parse_args()


if __name__ == "__main__":
    main()
