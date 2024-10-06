#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=W0102,E0712,C0103,R0903,C0301
""" SIMPLE API GATEWAY """

__updated__ = "2024-10-06 03:09:08"


import logging
from config import Config


def setup_logging():
    """
    Set up application-wide logging.
    """
    logging.basicConfig(
        level=Config.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    return logger
