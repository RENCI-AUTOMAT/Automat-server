from automat.config import config
from automat.core import Automat
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor


automat = Automat()


class App:
    async def __call__(self, scope, receive, send):
        scope_type = scope['type']
        if scope_type == 'http':
            await automat.handle_request(scope, receive, send)
        elif scope_type == 'lifespan':
            # otel asgi instrumentation middleware seems to break asgi lifespan
            # handling lifespan calls explicitly seems to fix that issue,
            # even though we're not really doing anything interesting
            # https://asgi.readthedocs.io/en/latest/specs/lifespan.html
            while True:
                message = await receive()
                if message['type'] == 'lifespan.startup':
                    ...  # Do some startup here!
                    await send({'type': 'lifespan.startup.complete'})
                elif message['type'] == 'lifespan.shutdown':
                    ...  # Do some shutdown here!
                    await send({'type': 'lifespan.shutdown.complete'})
                    return
        else:
            assert False


app = App()

if config.get("OTEL_ENABLED", "False").lower() == "true":
    from opentelemetry import trace
    from opentelemetry.sdk.resources import SERVICE_NAME, Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware

    resource = Resource(attributes={
        SERVICE_NAME: config.get("OTEL_SERVICE_NAME", "Automat"),
    })
    provider = TracerProvider(resource=resource)

    otel_host = config.get("OTEL_COLLECTOR_HOST", None)
    if otel_host:
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

        otel_port = config.get("OTEL_COLLECTOR_PORT", "4317")
        otel_endpoint = f'{otel_host}:{otel_port}'
        otel_exporter = OTLPSpanExporter(endpoint=f'{otel_endpoint}')
        processor = BatchSpanProcessor(otel_exporter)
    else:
        from opentelemetry.sdk.trace.export import ConsoleSpanExporter
        processor = BatchSpanProcessor(ConsoleSpanExporter())

    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # Enable OpenTelemetry instrumentation
    app = OpenTelemetryMiddleware(app)
    AioHttpClientInstrumentor().instrument()
