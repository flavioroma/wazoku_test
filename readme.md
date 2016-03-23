# Wazoku customer support developer test

## Description
This repo represents a stripped down version of our core ideas platform product 'spotlight'.
We have a customer export script named `user_activity_export.sh` which is run manually
and collates all the user activity for a given customer across the
site and emails the resulting data file to a named manager. The script can be run with the following:

    export DJANGO_SETTINGS_MODULE=exercise.settings
    bin/python -m scripts.user_activity_export \
      -c example.com \
      -e recipient@email.com


## Exercise 1

Clients now wish to receive a list of inactive users as well as active ones. Given the limitation
of the csv format, we propose generating an Excel document instead of a csv file. Use the
[openpyxl](https://openpyxl.readthedocs.org/) library to modify the code to produce an xlsx document
containing two sheets, the first mirrors the csv with a list of active users and their activity, the
second sheet contains a list of email addresses for those users with no activity on the site.
Feel free to refactor the code any way you see fit.

Please create a pull request for this work.

## Exercise 2

After a recent refactoring this code appears to have stopped working as
our customers are now reporting they are not receiving the emails when we run the script
(although occasionally the wrong manager does receive an email).
Please clone this repo, identify and fix the problem and issue a pull request for your fix.

Bonus marks will be awarded for the addition of tests against your fix

## Exercise 3

The current script is not particularly efficient against large customers. Can you improve on
the current code and reduce it's complexity from `O(N)` to `O(1)`. You might want to consider using [assertNumQueries]( https://docs.djangoproject.com/en/1.9/topics/testing/tools/#django.test.TransactionTestCase.assertNumQueries) to help you confirm this.

Please create a third pull request for this work.

## Getting started

To get started with the code, create a new virtualenv

    virtualenv .


Then install the dependencies:

    bin/pip install -r requirements.txt


Initialize an sqlite database

    bin/python manage.py migrate


The tests can be run with:

    bin/python manage.py test tests/
