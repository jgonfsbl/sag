#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=W0102,E0712,C0103,R0903,C0301
""" SIMPLE API GATEWAY """

__updated__ = "2024-10-06 03:09:25"


import uuid


def generate_trace_id():
    """
    Generate a UUID for request tracing.
    """
    return str(uuid.uuid4())
