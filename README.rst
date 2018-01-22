=========================
Simple Python date parser
=========================

Take an an input string representing a single date, and attempt to derive one or more valid datetime.date object(s)
allowing for ambiguity in input.

For example an input of '10/11/1980' might represent 10 November 1980 or 11 October 1980 in different locales.

Currently only supports triplet style inputs, e.g. '1/2/16', '1980-12-31', '20.01.2018'.

Two-digit years are currently parsed as literal

Usage
-----

parse_date(date_input)

Supported input formats
-----------------------

dd-mm-yyyy
mm-dd-yyyy
nn-nn-yyyy (i.e. ambiguous date/month order)

dd_mm_yy
mm_dd_yy
nn_nn_yy (i.e. ambiguous date/month order)

yyyy-mm-dd

Separators: '/', ' ', '-' and other punctuation

Output
------

Set of zero, one or more datetime.date objects
