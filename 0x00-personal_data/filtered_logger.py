#!/usr/bin/env python3
"""
Task:
    Write a function called filter_datum that returns the log
      message obfuscated:
    Arguments:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating all
          fields in the log line (message)
    The function should use a regex to replace occurrences of certain
      field values.
    filter_datum should be less than 5 lines long and use re.sub to perform
      the substitution with a single regex.

      def filter_datum(fields: List,
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    "" that returns the log message obfuscated ""
    message = message.split(separator)
    li = []
    for data in message:
        li.append(f"{data.split('=')[0]}={redaction}"
              if data.split('=')[0] in fields else data)
    return ';'.join(list(li))


def filter_datum(fields, redaction, message, separator):
    regex_pattern = r'({})'.format('|'.join(fields))
    return re.sub(regex_pattern, f"{regex_pattern}={redaction}", message)


def filter_datum(fields: List, redaction: str,
                 message: str, separator: str) -> str:
    ""that returns the log message obfuscated ""
    regex = re.compile(fr"({'|'.join(fields)})=[^{separator}]+")
    return regex.sub(fr"\1={redaction}", message)
"""
import re
import logging
from typing import List


# def filter_datum(fields, redaction, message, separator):
def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ that returns the log message obfuscated """
    return re.sub(fr'({"|".join(fields)})=[^{separator}]+',
                  fr'\1={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        """init function"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields or []

    def format(self, record: logging.LogRecord) -> str:
        """format function"""
        message = super(RedactingFormatter, self).format(record)
        for field in self.fields:
            message = message.replace(
                f"{field}={getattr(record, field)}",
                f"{field}={self.REDACTION}"
            )
        return message
