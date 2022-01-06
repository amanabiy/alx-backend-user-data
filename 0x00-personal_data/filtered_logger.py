#!/usr/bin/env python3
""" print filtered message Module """
import re


def filter_datum(fields, redaction, message, separtor):
    """ a filter that replaces fields with redaction in message"""
    for field in fields:
        message = re.sub(f'{field}=...{separtor}', f'{field}={redaction}{separtor}', message)
    return message
