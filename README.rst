=========================
Simple Python date parser
=========================

Takes an an input string representing a single date, and attempts to return one or more valid ``datetime.date``
object(s), allowing for ambiguity in input.

Currently only supports triplet style inputs, e.g. ``'1/2/16'``, ``'1980-12-31'``, ``'20.01.2018'``.

For example:

- an input of ``'10/11/1980'`` might represent 10 November 1980, or 11 October 1980 in different locales
- an input of ``'21/02/32'`` might represent 21 February 1932, or 21 February 2032 depending on context

This is designed primarily to handle user date inputs (as text, rather than a date picker) where if there is ambiguity,
the user can be prompted to confirm which date they intended, e.g.:

User input: 21/12/32
Response: "Did you mean 21 February 1932, or 21 February 2032?"

Supported input formats
=======================

+ ``'yyyy-mm-dd'``

- ``'dd-mm-yyyy'``
- ``'mm-dd-yyyy'``
- ``'nn-nn-yyyy'`` (i.e. ambiguous date/month order)


+ ``'dd-mm-yy'``
+ ``'mm-dd-yy'``
+ ``'nn-nn-yy'`` (i.e. ambiguous date/month order)

Permitted separators: '/', ' ', '-' and other punctuation

NB ``'yy-dd-mm'``, ``'yy-mm-dd'`` and thus ``'yy-nn-nn'`` and ``'nn-nn-nn'`` ambiguity aren't supported, as no
real-world examples have yet been located.


Usage
=====
::

    parse_date(date_input)
    parse_date(date_input, yy_leniency)

The optional ``yy_leniency`` parameter tunes the range of possible dates returned in response to a two-digit year value.


Output
======

A sorted list containing zero, one, two, three, four or six ``datetime.date`` objects.

Zero objects (i.e. an empty list) if no valid date can be parsed.
One object if the date is completely unambiguous.
Two objects if date/month order is ambiguous.
More objects may be returned if the optional ``yy_leniency`` parameter is > 0.

Examples
========

Unambiguous dates
-----------------

::

    >>> parse_date('13/05/1966')
    [datetime.date(1966, 5, 13)]
    # Input parsed as 'dd-mm-yyyy'
    # 13 May 1966

    >>> parse_date('5.13.1966')
    [datetime.date(1966, 5, 13)]
    # Input parsed as 'mm-dd-yyyy'
    # Also 13 May 1966

    >>> parse_date('01-01-1723')
    [datetime.date(1723, 1, 1)]
    # Input parsed as 'dd-mm-yyyy' or 'mm-dd-yyyy' - which give the same result in this case
    # 1 January 1723

Day-month ambiguity
-------------------

::

    >>> parse_date('05-06-1988')
    [datetime.date(1988, 5, 6), datetime.date(1988, 6, 5)]
    # Input parsed as 'dd-mm-yyyy' or 'mm-dd-yyyy'
    # 6 May 1988, or 5 June 1988?


Two-digit year handling and ``yy_leniency`` parameter
-----------------------------------------------------

When given a two-digit year, default behaviour is to return only the closest past/future match to present day,
or a pair of matches if there's day-month ambiguity. This is probably expected behaviour the vast majority of the time.

``yy_leniency <= 0`` will give the same result.

::

    >>> parse_date('14-02-15')
    [datetime.date(2015, 2, 14)]
    # Input parsed as 'dd-mm-yy'
    # 14 February 2015

    >>> parse_date('05-8-21')
    [datetime.date(2021, 5, 8), datetime.date(2021, 8, 5)]
    # Input parsed as 'dd-mm-yy' or 'mm-dd-yy'
    # 8 May 2021, or 5 August 2021?

``yy_leniency = 1`` returns also the next closest past/future match(es) to present day, two or four in total.
This might be desirable behaviour in an input field for a loan application.

::

    >>> parse_date('14-02-15', yy_leniency=1)
    [datetime.date(2015, 2, 14), datetime.date(2115, 2, 14)]
    # Input parsed as 'dd-mm-yy'
    # 14 February 2015, or 14 February 2115?

    >>> parse_date('05-8-21', yy_leniency=1)
    [datetime.date(1921, 5, 8), datetime.date(1921, 8, 5), datetime.date(2021, 5, 8), datetime.date(2021, 8, 5)]
    # Input parsed as 'dd-mm-yy' or 'mm-dd-yy'
    # 8 May 1921, 5 August 1921, 8 May 2021, or 5 August 2021?


``yy_leniency >= 2`` returns also the next closest past/future match(es) to present day, three or six in total.
This might be desirable behaviour in an input field for a genealogy application.

::

    >>> parse_date('14-02-15', yy_leniency=2)
    [datetime.date(1915, 2, 14), datetime.date(2015, 2, 14), datetime.date(2115, 2, 14)]
    # Input parsed as 'dd-mm-yy'
    # 14 February 1915, 14 February 2015, or 14 February 2115?

    >>> parse_date('05-8-21', yy_leniency=2)
    [datetime.date(1921, 5, 8), datetime.date(1921, 8, 5), datetime.date(2021, 5, 8), datetime.date(2021, 8, 5),
    datetime.date(2121, 5, 8), datetime.date(2121, 8, 5)]
    # Input parsed as 'dd-mm-yy' or 'mm-dd-yy'
    # 8 May 1921, 5 August 1921, 8 May 2021, 5 August 2021, 8 May 2121, or 5 August 2021?
