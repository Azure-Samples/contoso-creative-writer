import os
import json
import logging
import contextlib
from typing import AsyncIterator, List
from prompty.tracer import Tracer, PromptyTracer, console_tracer, to_dict
from opentelemetry import trace as oteltrace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

_tracer = "prompty"


@contextlib.contextmanager
def trace_span(name: str):
    tracer = oteltrace.get_tracer(_tracer)
    with tracer.start_as_current_span(name) as span:
        yield lambda key, value: span.set_attribute(
            key, json.dumps(value).replace("\n", "")
        )


def init_tracing(local_tracing: bool = False):

    if local_tracing:
        local_trace = PromptyTracer()
        Tracer.add("PromptyTracer", local_trace.tracer)
        # Tracer.add("ConsoleTracer", console_tracer)
    else:
        Tracer.add("OpenTelemetry", trace_span)

    azmon_logger = logging.getLogger("azure")
    azmon_logger.setLevel(logging.INFO)

    oteltrace.set_tracer_provider(TracerProvider())

    # Configure Azure Monitor as the Exporter
    app_insights = os.getenv("APPINSIGHTS_CONNECTIONSTRING")
    trace_exporter = AzureMonitorTraceExporter(connection_string=app_insights)

    # Add the Azure exporter to the tracer provider
    oteltrace.get_tracer_provider().add_span_processor(
        SimpleSpanProcessor(trace_exporter)
    )

    return oteltrace.get_tracer(_tracer)

