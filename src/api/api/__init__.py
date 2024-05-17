from flask import Flask
import logging
import api.get_article as get_article

import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import ParentBasedTraceIdRatio
from promptflow.tracing._integrations._openai_injector import inject_openai_api
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from promptflow.tracing import start_trace

def create_app():
    app = Flask(__name__)
    app.register_blueprint(get_article.bp)
    init_logging()
    return app


def init_logging():
    """Initializes logging."""

    # log to app insights if configured
    if 'APPINSIGHTS_CONNECTION_STRING' in os.environ:
        inject_openai_api()
        
        connection_string=os.environ['APPINSIGHTS_CONNECTION_STRING']
        trace.set_tracer_provider(TracerProvider(sampler=ParentBasedTraceIdRatio(1.0)))
        trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(AzureMonitorTraceExporter(connection_string=connection_string)))

    if 'PROMPTFLOW_TRACING_SERVER' in os.environ and os.environ['PROMPTFLOW_TRACING_SERVER'] != 'false':
        start_trace()

    

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Logging initialized.")
