#!/bin/python3

import argparse
import os
import re


import pathlib

currentPath = pathlib.Path(__file__).parent.resolve()

if currentPath.__str__() == "/usr/bin":
    hostFileLoc = "/etc/hosts"
else:
    # for testing using ./etc/hosts
    hostFileLoc = "./etc/hosts"


class SColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def is_valid_domain(domain):
    regex = ("^((?!-)[A-Za-z0-9-]"
             "{1,63}(?<!-)\\.)"
             "+[A-Za-z]{2,6}")
    p = re.compile(regex)
    if not domain:
        return False
    if re.search(p, domain):
        return True
    else:
        return False


def ban_domain():
    check_domain_validity = is_valid_domain(args.domain_name)
    if check_domain_validity:
        regex = f"^# 127.0.0.1\s+{args.domain_name}"
        domainReg = re.compile(regex)
        with open(hostFileLoc, "r+") as file:
            lines = file.readlines()
            never_created_regex = f'(.*?)127.0.0.1\s+{args.domain_name}(.*?)'
            ever_created = re.search(never_created_regex, ''.join(lines).strip())
        with open(hostFileLoc, "w") as file:
            for index, line in enumerate(lines):
                domain_check = re.search(domainReg, line.strip())
                if domain_check:
                    lines[index] = re.sub('#\s+', '', line)
            if not ever_created:
                lines.append(f"\n127.0.0.1    {args.domain_name}")

            file.write("".join(lines))

        os.system('/bin/systemctl restart network-manager')
    else:
        print(f"{SColor.WARNING}Invalid domain name provided: '{args.domain_name}'{SColor.ENDC}")


def unban_domain():
    check_domain_validity = is_valid_domain(args.domain_name)
    if check_domain_validity:
        regex = f"^127.0.0.1\s+{args.domain_name}"
        domainReg = re.compile(regex)
        with open(hostFileLoc, "r") as file:
            lines = file.readlines()
        with open(hostFileLoc, "w") as file:
            for index, lastLine in enumerate(lines):
                if re.search(domainReg, lastLine):
                    lines[index] = f"# {lastLine}"
            file.write("".join(lines))
    else:
        print(f"{SColor.WARNING}Invalid domain name provided: '{args.domain_name}'{SColor.ENDC}")


# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')

parser.add_argument('domain_name', type=str,
                    help='The domain name that you wanna interact with.')
parser.add_argument('-u', '--unban-domain', action='store_true',
                    help='Do you wanna unban it?')
parser.add_argument('-b', '--ban-domain', action='store_true',
                    help='Do you wanna ban it?')
parser.add_argument('-c', '--check-domain', action='store_true', default=True,
                    help='Checks if the domain you are sending is valid or not!')

args = parser.parse_args()

try:
    if args.check_domain and (not args.ban_domain and not args.unban_domain):
        is_valid = is_valid_domain(args.domain_name)
        message = f"{SColor.OKBLUE}Yes, domain is valid for un/banning." if is_valid else f"{SColor.FAIL}Nope, domain isn't valid for un/banning."
        print(f"{message}{SColor.ENDC}")

    if args.ban_domain:
        ban_domain()

    if args.unban_domain:
        unban_domain()

except PermissionError:
    print(f"{SColor.FAIL}You don't have any permissions to do this, please use admin privileges.{SColor.ENDC}")
