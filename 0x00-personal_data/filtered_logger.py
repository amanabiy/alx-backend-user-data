#!/usr/bin/env python3
""" print filtered message Module """
import re
import logging
from typing import List
from typing_extensions import Self
PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'ip')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ a filter that replaces fields with redaction in message"""
    for field in fields:
        message = re.sub(f'{field}=.+?{separator}',
                         f'{field}={redaction}{separator}', message)
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


def get_logger() -> logging.Logger:
    """
    returns logger for user_data
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    formatter = RedactingFormatter(list(PII_FIELDS))

    st_handler = logging.StreamHandler()
    st_handler.setFormatter(formatter)
    logger.addHandler(st_handler)
    return logger
