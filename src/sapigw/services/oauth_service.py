#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=W0102,E0712,C0103,R0903,C0301,R1710
""" SIMPLE API GATEWAY """

__updated__ = "2024-10-06 22:37:21"

import logging
from functools import lru_cache
import requests
from flask import request, abort
from config import Config

from jose import jwt

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_jwks():
    """
    Fetch JWKS from the OAuth2 provider.
    """
    try:
        response = requests.get(Config.OAUTH2_JWKS_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error("Error fetching JWKS: %s", e)
        abort(500, description="Internal server error")


def oauth2_scheme():
    """
    OAuth2 token validation middleware.
    """
    auth_header = request.headers.get("Authorization", None)
    if not auth_header or not auth_header.startswith("Bearer "):
        logger.error("Missing or invalid Authorization header.")
        abort(401, description="Missing or invalid Authorization header")
        return None  # Explicitly return None to indicate no token

    token = auth_header.split(" ")[1]

    # Validate token
    try:
        jwks = get_jwks()
        # Decode and validate JWT token
        decoded_token = jwt.decode(token, jwks, options={"verify_aud": False})
        logger.info("Valid token: %s", decoded_token)
        return decoded_token  # Return the decoded token
    except jwt.JWTError as e:
        logger.error("Token validation failed: %s", e)
        abort(401, description="Invalid token")
        return None  # Explicitly return None when token validation fails
