#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=W0102,E0712,C0103,R0903,C0301
""" SIMPLE API GATEWAY """

__updated__ = "2024-10-06 03:13:53"


from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config


# Initialize the Limiter
limiter = Limiter(key_func=get_remote_address)


def rate_limit(requests_per_minute: int = 0):
    """
    Convert integer rate limit to the 'requests per minute' format.
    """
    if requests_per_minute is None:
        # Use the default from config if not provided
        requests_per_minute = Config.DEFAULT_RATE_LIMIT

    return limiter.limit(f"{requests_per_minute} per minute")
