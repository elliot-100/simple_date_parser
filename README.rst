=========================
Simple Python date parser
=========================

Take an an input string representing a single date, and attempt to derive one or more valid datetime.date object(s) allowing for ambiguity in input.

Currently only supports triplet style inputs, e.g. '1/2/16', '1980-12-31', '20.01.2018'.

For example an input of '10/11/1980' might represent 10 November 1980 or 11 October 1980 in different locales.

Supported input formats
-----------------------

- dd-mm-yyyy
- mm-dd-yyyy
- nn-nn-yyyy (i.e. ambiguous date/month order)

- dd_mm_yy
- mm_dd_yy
- nn_nn_yy (i.e. ambiguous date/month order)

- yyyy-mm-dd

Permitted separators: '/', ' ', '-' and other punctuation

Output
------

Sorted list of zero, one or more datetime.date objects


Usage
-----

parse_date(date_input)

Examples
--------

> parse_date("01-01-1723")
[datetime.date(1723, 1, 1)]

> parse_date("05-06-1988")
[datetime.date(1988, 5, 6), datetime.date(1988, 6, 5)]

> parse_date("0001-1-1")
[datetime.date(1, 1, 1)]

> parse_date("1-1-1")
[datetime.date(1, 1, 1), datetime.date(1901, 1, 1), datetime.date(2001, 1, 1)]


