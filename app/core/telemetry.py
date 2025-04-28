import logging
from opentelemetry import trace
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import os

def setup_telemetry(app, service_name: str = "fastapi-example"):
    """Configure OpenTelemetry for the FastAPI application."""
    try:
        # Create a resource
        resource = Resource.create({
            "service.name": service_name,
        })
        
        # Configure OTLP exporter with detailed settings
        endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "alloy.observability.svc.cluster.local:4317")
        insecure = os.getenv("OTEL_EXPORTER_OTLP_INSECURE", "true").lower() == "true"
        
        # Create and set up the logger provider
        logger_provider = LoggerProvider(resource=resource)
        
        # Configure OTLP log exporter
        otlp_log_exporter = OTLPLogExporter(
            endpoint=endpoint,
            insecure=insecure,
            timeout=5
        )
        
        log_processor = BatchLogRecordProcessor(
            otlp_log_exporter,
            schedule_delay_millis=5000,
            max_export_batch_size=512,
            export_timeout_millis=30000,
        )
        logger_provider.add_log_record_processor(log_processor)
        
        # Configure the root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        # Remove any existing handlers to avoid duplicate logs
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Set up logging instrumentation
        LoggingInstrumentor().instrument(
            logger_provider=logger_provider,
            set_logging_format=True,
            log_level=logging.INFO
        )
        
        # Configure application loggers to propagate to root
        app_logger = logging.getLogger("app")
        app_logger.setLevel(logging.INFO)
        app_logger.propagate = True
        
        # Instrument FastAPI with tracing disabled
        FastAPIInstrumentor.instrument_app(app)
        
        # Log startup message
        app_logger.info(
            f"Starting {service_name} with OpenTelemetry instrumentation (tracing disabled). "
            f"OTEL endpoint: {endpoint}, "
            f"Insecure mode: {insecure}"
        )
            
    except Exception as e:
        logging.error(f"Failed to set up telemetry: {e}", exc_info=True)
        raise 