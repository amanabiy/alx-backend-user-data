#!/usr/bin/env python3
""" print filtered message Module """
import re
import logging
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separtor: str) -> str:
    """ a filter that replaces fields with redaction in message"""
    for field in fields:
        message = re.sub(f'{field}=.+?{separtor}',
                         f'{field}={redaction}{separtor}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ format """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
