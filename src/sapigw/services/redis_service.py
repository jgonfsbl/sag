#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=W0102,E0712,C0103,R0903,C0301,W0212,W1203
""" SIMPLE API GATEWAY """

__updated__ = "2024-10-06 03:44:56"


import logging
import redis
from config import Config


logger = logging.getLogger(__name__)

# Set up Redis connection pool
redis_pool = redis.ConnectionPool(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=Config.REDIS_DB,
    max_connections=Config.REDIS_POOL_SIZE,
)

# Redis client using the connection pool
redis_client = redis.Redis(connection_pool=redis_pool)


def log_pool_stats():
    """
    Log details about the Redis connection pool.
    """
    logger.info(
        "Connection pool max connections: %d", redis_pool.max_connections
    )  # Lazy logging
    # Skipping protected attributes _available_connections and _in_use_connections
    # as it's not recommended to access them directly in production code
    logger.info(
        f"Currently available connections: {len(redis_pool._available_connections)}"
    )
    logger.info(f"Currently in-use connections: {len(redis_pool._in_use_connections)}")


def register_service(service_name, domain, url_path, location):
    """
    Register a new service in Redis with domain, URL path, and container location.
    Example: register_service('service1', 'example.com', '/api/v1', 'localhost:5000')
    """
    log_pool_stats()  # Log pool stats before the operation
    redis_key = f"{service_name}:{domain}:{url_path}"
    redis_client.rpush(redis_key, location)
    log_pool_stats()  # Log pool stats after the operation


def get_service_location(domain, url_path):
    """
    Retrieve the container location for a service based on the domain and URL path.
    Implements round-robin selection if multiple containers exist.
    Tries to match the most specific URL path first.
    Example: get_service_location('example.com', '/api/v1/specificresource')
    """

    # First try to find the most specific match for the domain and full URL path
    specific_key = f"*:{domain}:{url_path}"
    specific_keys = redis_client.keys(specific_key)

    if specific_keys:
        # If a specific match is found, apply round-robin
        service_key = specific_keys[0]
        location = redis_client.lpop(service_key)  # Pop the first instance
        redis_client.rpush(service_key, location)  # Push it back to the end of the list
        return location.decode("utf-8")

    # If no specific match is found, fall back to a more general path (e.g., /api/v1)
    general_path = "/".join(
        url_path.split("/")[:3]
    )  # Generalize path to /api/v1 or similar
    general_key = f"*:{domain}:{general_path}"
    general_keys = redis_client.keys(general_key)

    if general_keys:
        service_key = general_keys[0]
        location = redis_client.lpop(service_key)  # Pop the first instance
        redis_client.rpush(service_key, location)  # Push it back to the end of the list
        return location.decode("utf-8")

    return None
