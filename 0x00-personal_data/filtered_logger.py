#!/usr/bin/env python3
""" print filtered message Module """
import re
import logging
from typing import List
from typing_extensions import Self
import mysql.connector
import os


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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
    """ returns logger for user_data """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = RedactingFormatter(list(PII_FIELDS))
    st_handler = logging.StreamHandler()
    st_handler.setFormatter(formatter)
    logger.addHandler(st_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns connector to a database """
    db_pass = os.environ.get('PERSONAL_DATA_DB_PASSWORD')
    db_user = os.environ.get('PERSONAL_DATA_DB_USERNAME')
    db_host = os.environ.get('PERSONAL_DATA_DB_HOST')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')
    return mysql.connector.connect(user=db_user, password=db_pass,
                                   host=db_host, database=db_name)
