# coding=utf-8
import re
import datetime


def parse_date(date_input, yy_leniency=0):
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
    dates2 = set()

    if word_patterns == ['nn', 'nn', 'nnnn']:
        try:
            # parse input as mm-dd-yyyy
            dates.add(datetime.date(words[2], words[0], words[1]))
        except ValueError:
            pass
        try:
            # parse input as dd-mm-yyyy
            dates.add(datetime.date(words[2], words[1], words[0]))
        except ValueError:
            pass

    elif word_patterns == ['nnnn', 'nn', 'nn']:
        try:
            # parse input as yyyy-mm-dd
            dates.add(datetime.date(words[0], words[1], words[2]))
        except ValueError:
            pass

    elif word_patterns == ['nn', 'nn', 'nn']:
        today = datetime.date.today()
        century = today.year // 100 * 100

        # parse input as dd-mm-nnyy

        try:
            dates.add(datetime.date(century - 100 + words[2], words[1], words[0]))
        except ValueError:
            pass

        try:
            dates.add(datetime.date(century + words[2], words[1], words[0]))
        except ValueError:
            pass

        try:
            dates.add(datetime.date(century + 100 + words[2], words[1], words[0]))
        except ValueError:
            pass

        if yy_leniency <= 0:
            dates = list(dates)
            dates.sort(key=lambda d: abs(d - today))
            if dates:
                dates = [dates[0]]

        # parse input as mm-dd-nnyy

        try:
            dates2.add(datetime.date(century - 100 + words[2], words[0], words[1]))
        except ValueError:
            pass

        try:
            dates2.add(datetime.date(century + words[2], words[0], words[1]))
        except ValueError:
            pass

        try:
            dates2.add(datetime.date(century + 100 + words[2], words[0], words[1]))
        except ValueError:
            pass

        if yy_leniency <= 0:
            dates2 = list(dates2)
            dates2.sort(key=lambda d: abs(d - today))
            if dates2:
                dates2 = [dates2[0]]

    else:
        pass  # TODO: consider error handling

    dates = list(dates)
    dates2 = list(dates2)
    return sorted(dates + dates2)
