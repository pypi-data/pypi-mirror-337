import asyncio
import logging
import sys

from baseten_benchmarks.input_handler import InputHandler
from baseten_benchmarks import parse_args
from baseten_benchmarks.request_handler import RequestHandler
from baseten_benchmarks.benchmark_executor import BenchmarkExecutor
from baseten_benchmarks.generic_rest_provider import get_llm_provider


logger = None


async def main(args):
    # Create initial input handler with index 0
    input_handler = InputHandler(args, prompt_count_index=0)
    llm_provider = get_llm_provider(args)
    request_handler = RequestHandler(llm_provider, args)
    request_handler.input_handler = input_handler  # Update input handler

    executor = BenchmarkExecutor(args, request_handler, input_handler)
    output = await executor.execute()

    logger.info(output)
    logger.info(f"Detailed results saved to {args.model}/{args.output_file}")


def run():
    args = parse_args.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )
    global logger
    logger = logging.getLogger(__name__)
    asyncio.run(main(args))


if __name__ == "__main__":
    run()
