# coding=utf-8
import re
import datetime


def attempt_date_append(date_list, year, month, date):
    """ Wraps datetime.date creation to suppress errors on invalid dates. """

    try:
        date_list.append(datetime.date(year, month, date))
    except ValueError:
        pass


def parse_date(date_input, yy_leniency=0):
    """ Attempt to derive one or more valid datetime.date object(s) from an input string representing a single date,
        allowing for ambiguity. """

    words = re.split('\W', date_input)[:3]  # first 3 words, separated by any punctuation
    word_patterns = []
    dates = []
    dates2 = []

    for i in range(len(words)):
        if words[i].isdigit:
            if len(words[i]) <= 2:
                word_patterns.insert(i, 'nn')
            elif len(words[i]) <= 4:
                word_patterns.insert(i, 'nnnn')
        words[i] = int(words[i])

    if word_patterns == ['nn', 'nn', 'nnnn']:
        # parse input as mm-dd-yyyy
        attempt_date_append(dates, words[2], words[0], words[1])
        if words[0] != words[1]:
            # parse input as dd-mm-yyyy
            attempt_date_append(dates, words[2], words[1], words[0])

    elif word_patterns == ['nnnn', 'nn', 'nn']:
        # parse input as yyyy-mm-dd
        attempt_date_append(dates, words[0], words[1], words[2])

    elif word_patterns == ['nn', 'nn', 'nn']:
        today = datetime.date.today()
        century = today.year // 100 * 100

        # parse input as dd-mm-nnyy

        attempt_date_append(dates, words[2] + century - 100, words[1], words[0])
        attempt_date_append(dates, words[2] + century, words[1], words[0])
        attempt_date_append(dates, words[2] + century + 100, words[1], words[0])

        dates.sort(key=lambda d: abs(d - today))

        if yy_leniency <= 0:
            dates = dates[0:1]
        elif yy_leniency == 1:
            dates = dates[0:2]

        if words[0] != words[1]:

            # mm and dd values are distinct
            # parse input as mm-dd-nnyy

            attempt_date_append(dates2, words[2] + century - 100, words[0], words[1])
            attempt_date_append(dates2, words[2] + century, words[0], words[1])
            attempt_date_append(dates2, words[2] + century + 100, words[0], words[1])

            dates2.sort(key=lambda d: abs(d - today))

            if yy_leniency <= 0:
                dates2 = dates2[0:1]
            elif yy_leniency == 1:
                dates2 = dates2[0:2]

    else:
        pass

    return sorted(dates + dates2)
