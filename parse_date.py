# coding=utf-8
import re
import datetime


def attempt_to_create_date(date_list, arg1, arg2, arg3):
    try:
        # parse input as mm-dd-yyyy
        date_list.append(datetime.date(arg1, arg2, arg3))
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
        attempt_to_create_date(dates, words[2], words[0], words[1])
        if words[0] != words[1]:
            # parse input as dd-mm-yyyy
            attempt_to_create_date(dates, words[2], words[1], words[0])

    elif word_patterns == ['nnnn', 'nn', 'nn']:
        # parse input as yyyy-mm-dd
        attempt_to_create_date(dates, words[0], words[1], words[2])

    elif word_patterns == ['nn', 'nn', 'nn']:
        today = datetime.date.today()
        century = today.year // 100 * 100

        # parse input as dd-mm-nnyy

        attempt_to_create_date(dates, words[2], words[1], words[0])
        attempt_to_create_date(dates, words[2] + century - 100, words[1], words[0])
        attempt_to_create_date(dates, words[2] + century, words[1], words[0])
        attempt_to_create_date(dates, words[2] + century + 100, words[1], words[0])

        # dates = list(dates)
        dates.sort(key=lambda d: abs(d - today))

        if yy_leniency <= 0:
            dates = dates[0:1]
        elif yy_leniency == 1:
            dates = dates[0:2]
        elif yy_leniency == 2:
            dates = dates[0:3]
        elif yy_leniency == 3:
            dates = dates[0:4]

        print('dates: ' + str(dates))

        if words[0] != words[1]:
            # mm and dd values are distinct
            # parse input as mm-dd-nnyy

            attempt_to_create_date(dates2, words[2], words[0], words[1])
            attempt_to_create_date(dates2, words[2] + century - 100, words[0], words[1])
            attempt_to_create_date(dates2, words[2] + century, words[0], words[1])
            attempt_to_create_date(dates2, words[2] + century + 100, words[0], words[1])

            # extended_dates = list(extended_dates)
            dates2.sort(key=lambda d: abs(d - today))

            if yy_leniency <= 0:
                dates2 = dates2[0:1]
            elif yy_leniency == 1:
                dates2 = dates2[0:2]
            elif yy_leniency == 2:
                dates2 = dates2[0:3]
            elif yy_leniency == 3:
                dates2 = dates2[0:4]

            print('dates2: ' + str(dates2))

    else:
        pass  # TODO: consider error handling

    print('dates+dates2: ' + str(sorted(dates + dates2)))
    return sorted(dates + dates2)


######

parse_date("13-13-40", 3)
