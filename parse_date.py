# coding=utf-8
import re
import datetime

century_bases = (0, 1900, 2000)


def parse_date(date_input):
    """ Attempt to derive one or more valid datetime.date object(s) from an input string representing a single date,
        allowing for ambiguity. """

    words = re.split('\W', date_input)[:3]  # first 3 words, separated by any punctuation
    word_patterns = []

    for i in range(len(words)):
        if words[i].isdigit:
            if len(words[i]) <= 2:
                word_patterns.insert(i, 'nn')
            elif len(words[i]) <= 4:
                word_patterns.insert(i, 'nnnn')
        words[i] = int(words[i])

    dates = set()

    if word_patterns == ['nn', 'nn', 'nnnn']:
        try:
            dates.add(datetime.date(words[2], words[0], words[1]))  # mm-dd-yyyy
        except ValueError:
            pass
        try:
            dates.add(datetime.date(words[2], words[1], words[0]))  # dd-mm-yyyy
        except ValueError:
            pass

    if word_patterns == ['nnnn', 'nn', 'nn']:
        try:
            dates.add(datetime.date(words[0], words[1], words[2]))  # yyyy-mm-dd
        except ValueError:
            pass

    if word_patterns == ['nn', 'nn', 'nn']:
        for cb in century_bases:
            try:
                dates.add(datetime.date(cb + words[2], words[1], words[0]))
                # dd-mm-yy (pre-1000CE), dd-mm-19yy, dd-mm-20yy
            except ValueError:
                pass
            try:
                dates.add(datetime.date(cb + words[2], words[0], words[1]))
                # mm-dd-yy (pre-1000CE), mm-dd-19yy, mm-dd-20yy
            except ValueError:
                pass

    return sorted(list(dates))
