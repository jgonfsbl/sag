#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=W0102,E0712,C0103,R0903,C0301
""" SIMPLE API GATEWAY """

__updated__ = "2024-10-06 22:35:37"


from os import environ
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    """
    Set Flask configuration vars from .env file or environment variables.
    """

    # General
    FLASK_APP = environ.get("FLASK_APP", "app.py")
    FLASK_ENV = environ.get("FLASK_ENV", "production")
    FLASK_DEBUG = environ.get("FLASK_DEBUG", "False").lower() == "true"
    FLASK_HOST = environ.get("FLASK_HOST", "localhost")
    FLASK_PORT = environ.get("FLASK_PORT", "5000")
    LOG_LEVEL = environ.get("LOG_LEVEL", "DEBUG")

    # APIs
    SECRET_KEY = environ.get("SECRET_KEY", "you-will-never-guess-me")

    # OAuth2
    OAUTH2_PROVIDER_URL = environ.get("OAUTH2_PROVIDER_URL", "https://idp.example.com")
    OAUTH2_JWKS_URL = f"{OAUTH2_PROVIDER_URL}/.well-known/jwks.json"
    OAUTH2_CACHE_TIMEOUT = int(environ.get("OAUTH2_CACHE_TIMEOUT", "300"))

    # Redis
    REDIS_HOST = environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = int(environ.get("REDIS_PORT", 6379))
    REDIS_DB = int(environ.get("REDIS_DB", 0))
    REDIS_POOL_SIZE = int(environ.get("REDIS_POOL_SIZE", 10))
    REDIS_CACHE_TIMEOUT = int(environ.get("REDIS_CACHE_TIMEOUT", 300))

    # Rate Limiting; default to 100 requests/minute
    DEFAULT_RATE_LIMIT = int(environ.get("DEFAULT_RATE_LIMIT", 100))

    # Prometheus
    PROMETHEUS_ENABLED = environ.get("PROMETHEUS_ENABLED", "True").lower() == "true"
