#!/usr/bin/env python3
""" print filtered message Module """
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separtor: str) -> str:
    """ a filter that replaces fields with redaction in message"""
    for field in fields:
        message = re.sub(f'{field}=...{separtor}',
                         f'{field}={redaction}{separtor}', message)
    return message
