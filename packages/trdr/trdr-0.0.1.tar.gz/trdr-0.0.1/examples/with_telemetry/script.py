import asyncio
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from trdr.core.bar_provider.yf_bar_provider.yf_bar_provider import YFBarProvider
from trdr.core.security_provider.security_provider import SecurityProvider
from trdr.core.broker.mock_broker.mock_broker import MockBroker
from trdr.core.trading_engine.trading_engine import TradingEngine
from trdr.core.trading_context.trading_context import TradingContext
from trdr.core.broker.pdt.nun_strategy import NunStrategy

if __name__ == "__main__":

    async def main():
        tracer_provider = TracerProvider()
        """
        I run the collector as a container locally for testing purposes.
        """
        otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
        span_processor = BatchSpanProcessor(otlp_exporter, max_export_batch_size=20)
        tracer_provider.add_span_processor(span_processor)
        trace.set_tracer_provider(tracer_provider)
        tracer = trace.get_tracer("trdr")
        try:
            pdt_strategy = NunStrategy.create(tracer)
            async with await MockBroker.create(pdt_strategy, tracer) as broker:
                bar_provider = await YFBarProvider.create(["TSLA"], tracer)
                security_provider = await SecurityProvider.create(bar_provider, tracer)
                context = await TradingContext.create(security_provider, broker, tracer)
                engine = await TradingEngine.create(
                    "first-strat", context, strategies_dir="../strategies", tracer=tracer
                )
                await engine.execute()

        except Exception as e:
            print(e)

    asyncio.run(main())
