"""
OpenTelemetry configuration for Django application.

Usage:
    Add to Django settings.py or wsgi.py:
        from observability.opentelemetry_config import setup_opentelemetry
        setup_opentelemetry()

    Or import in manage.py before Django setup:
        from observability.opentelemetry_config import setup_opentelemetry
        setup_opentelemetry()
"""

import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION, DEPLOYMENT_ENVIRONMENT
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.mysql import MySQLInstrumentor


def setup_opentelemetry():
    """Initialize OpenTelemetry tracing with OTLP gRPC exporter."""

    service_name = os.environ.get("OTEL_SERVICE_NAME", "ejemplo-python")
    service_version = os.environ.get("OTEL_SERVICE_VERSION", "1.0.0")
    environment = os.environ.get("OTEL_ENVIRONMENT", os.environ.get("APP_ENV", "development"))
    otlp_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317")

    resource = Resource.create({
        SERVICE_NAME: service_name,
        SERVICE_VERSION: service_version,
        DEPLOYMENT_ENVIRONMENT: environment,
        "service.namespace": "ejemplo-python",
    })

    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    DjangoInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    MySQLInstrumentor().instrument()
