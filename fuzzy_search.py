#!/usr/bin/env python3
import argparse
from versions import graphic_version
from versions import console_version
from PyQt5.QtWidgets import QApplication
import sys


def parse_args():
    parser = argparse.ArgumentParser(description='Fuzzy search in text.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--console', action='store_true',
                       help='console mode. '
                       '[-r] - register-check. '
                       '[-v] - row_view. '
                       'TEXTFILE - file with text. '
                       '[WORDSFILE] - file with words.'
                       ' If no WORDSFILE, then get words from stdin.')
    group.add_argument('-g', '--graphics', action='store_true',
                       help='graphic mode')

    args, rest = parser.parse_known_args()
    if args.console:
        console_parser = argparse.ArgumentParser(parents=[parser],
                                                 add_help=False)
        console_parser.add_argument('-r', '--register-check',
                                    action='store_true')
        console_parser.add_argument('-v', '--row-view', action='store_true')
        console_parser.add_argument('TEXTFILE', type=str)
        console_parser.add_argument('WORDSFILE', type=argparse.FileType('r'),
                                    default=sys.stdin, nargs='?')
        args = console_parser.parse_args()
    elif rest:
        parser.error("unexpected arguments: " + str(rest))
    return args


def start_search(args):
    if args.graphics:
        graphic_version.start_application()
    if args.console:
        app = QApplication(sys.argv)
        if args.WORDSFILE == sys.stdin:
            try:
                words = input()
            except KeyboardInterrupt:
                sys.exit(0)
            cv = console_version.ConsoleVersion(
                args.TEXTFILE, words,
                args.register_check, args.row_view)
            cv.search_words_in_text()
            sys.exit(app.exec_())
        else:
            cv = console_version.ConsoleVersion(
                args.TEXTFILE, args.WORDSFILE,
                args.register_check, args.row_view)
            cv.search_words_in_text()
            sys.exit(app.exec_())


if __name__ == '__main__':
    args = parse_args()
    start_search(args)
