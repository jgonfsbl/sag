#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=W0102,E0712,C0103,R0903,C0301
""" SIMPLE API GATEWAY """

__updated__ = "2024-10-06 03:09:38"


from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from config import Config
from services.gateway_service import gateway, circuit_breaker_error
from services.oauth_service import oauth2_scheme


app = Flask(__name__)
app.config.from_object(Config)

# Prometheus Metrics
metrics = PrometheusMetrics(app)
metrics.info("app_info", "API Gateway service", version="1.0")

# Expose default metrics at `/metrics`
if Config.PROMETHEUS_ENABLED:
    metrics.start_http_server(
        8000
    )  # Use a separate port for scraping Prometheus metrics

# Set up routes
app.add_url_rule("/", "circuit_breaker_error", circuit_breaker_error)
app.add_url_rule(
    "/<service>/<path:path>",
    "gateway",
    gateway,
    methods=["GET", "POST", "PUT", "DELETE"],
)

# OAuth2 protection
app.before_request(oauth2_scheme)

if __name__ == "__main__":
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=Config.FLASK_DEBUG)
