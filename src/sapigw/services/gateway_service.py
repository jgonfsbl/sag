#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=W0102,E0712,C0103,R0903,C0301
""" SIMPLE API GATEWAY """

__updated__ = "2024-10-06 03:10:01"


from flask import request, jsonify, render_template
import requests
from services.redis_service import get_service_location
from utils.trace import generate_trace_id
from utils.logger import setup_logging
from utils.rate_limiter import rate_limit
from flask_caching import Cache
from prometheus_flask_exporter import PrometheusMetrics

logger = setup_logging()

# Initialize caching
cache = Cache()

# Prometheus Metrics
metrics = PrometheusMetrics.for_app_factory()

# Circuit breaker flag
circuit_breaker_triggered = False


def cache_key():
    """
    Generate cache key based on the request path.
    """
    return request.full_path


@rate_limit(100)
@metrics.counter(
    "gateway_requests",
    "Request count for gateway",
    labels={"service": lambda: request.view_args["service"]},
)
@metrics.histogram(
    "gateway_response_time",
    "Response time for gateway requests",
    labels={"service": lambda: request.view_args["service"]},
)
def gateway(service, path):
    """
    Main API Gateway route with tenant routing based on domain, URL path, and container location.
    """
    if circuit_breaker_triggered:
        return (
            render_template(
                "error.html", message="Service Unavailable. Please try again later."
            ),
            503,
        )

    trace_id = generate_trace_id()
    domain = request.host
    logger.info(
        f"Request Trace ID {trace_id} - Incoming request to {service} on domain {domain} for path: {path}, Method: {request.method}"
    )

    # Find the correct service location based on domain and path
    service_location = get_service_location(domain, path)
    if service_location is None:
        logger.error(
            f"Request Trace ID {trace_id} - Unknown service or route for domain {domain} and path {path}"
        )
        return jsonify({"error": "Unknown service or route"}), 404

    full_url = f"http://{service_location}{path}"

    try:
        response = requests.request(
            method=request.method,
            url=full_url,
            headers={key: value for key, value in request.headers if key != "Host"},
            data=request.get_data(),
            params=request.args,
        )

        logger.info(
            f"Request Trace ID {trace_id} - Response from {full_url}: Status {response.status_code}"
        )
        return (response.content, response.status_code, response.headers.items())

    except requests.exceptions.RequestException as e:
        logger.error(
            f"Request Trace ID {trace_id} - Error connecting to {full_url}: {e}"
        )
        return jsonify({"error": "Service unavailable"}), 503


def circuit_breaker_error():
    """
    Show error page when circuit breaker is triggered.
    """
    return (
        render_template(
            "error.html", message="Service Unavailable. Please try again later."
        ),
        503,
    )
