import argparse
import sys
import os

from . import bot

if __name__ == '__main__':
    parser = argparse.ArgumentParser('meowclock')
    parser.add_argument('-u', '--username', type=str, help='the username (email) to log in as', required=True)
    parser.add_argument('-p', '--password', type=str, help='the password to use to log in', required=True)
    parser.add_argument('-d', '--domain', type=str, help='the domain to log into', default='botsin.space')
    parser.add_argument('-s', '--data', type=str, help='where metadata should be stored', default=None)

    args = parser.parse_args(sys.argv[1:])

    if args.data:
        os.chdir(args.data)

    try:
        bot.run(args.username, args.password, args.domain)
    except KeyboardInterrupt:
        print('Exiting...')
