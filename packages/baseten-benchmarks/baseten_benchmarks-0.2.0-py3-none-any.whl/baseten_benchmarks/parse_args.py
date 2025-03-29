import argparse
from datetime import datetime
import json


def parse_args():
    parser = argparse.ArgumentParser(description="LLM Benchmarking Tool")
    parser.add_argument(
        "--backend",
        type=str,
        required=True,
        help="Backend to benchmark (e.g., 'generic')",
    )
    parser.add_argument(
        "--log_level",
        type=str,
        default="INFO",
        help="Logging level (DEBUG, INFO)",
    )
    parser.add_argument("--api_url", type=str, required=True, help="API endpoint URL")
    parser.add_argument("--model", type=str, required=False, help="Model name or path")
    parser.add_argument(
        "--duration",
        type=int,
        default=None,
        help="Duration of the benchmark in seconds (optional)",
    )
    parser.add_argument(
        "--num_prompts",
        type=int,
        nargs="+",
        default=[100],
        help="Number of prompts to process. Can be multiple values to match concurrency levels.",
    )
    parser.add_argument(
        "--output_len", type=int, default=50, help="Maximum output length"
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        nargs="+",
        default=None,
        help="Number of concurrent requests. Can be multiple values.",
    )
    parser.add_argument(
        "--request_rate", type=float, default=None, help="Number of requests per second"
    )
    parser.add_argument(
        "--random_input", type=int, default=30, help="Input length for random dataset"
    )
    parser.add_argument(
        "--disable_tqdm", action="store_true", help="Disable progress bar"
    )
    parser.add_argument(
        "--extra_request_body",
        type=str,
        help="Extra parameters for the request body (JSON format)",
    )
    parser.add_argument("--stream", action="store_true", help="Use streaming mode")
    parser.add_argument(
        "--input_file", type=str, help="Path to input file containing prompts"
    )
    parser.add_argument(
        "--input_type",
        type=str,
        choices=["random", "file", "stdin", "custom"],
        default="random",
        help="Type of input to use",
    )
    parser.add_argument(
        "--output_file", type=str, help="Output file for results (CSV format)"
    )
    parser.add_argument(
        "--disable_warmup", action="store_true", help="Disable warmup requests"
    )
    parser.add_argument(
        "--warmup_requests",
        type=int,
        default=1,
        help="Number of warmup requests to perform",
    )
    parser.add_argument(
        "--tokenizer", type=str, help="Name of the AutoTokenizer to use (e.g., 'gpt2')"
    )
    parser.add_argument(
        "--api_key", type=str, required=True, help="API key for authentication"
    )
    parser.add_argument(
        "--prompt_style",
        type=str,
        choices=["prompt", "messages"],
        default="prompt",
        help="Style of prompt to use: 'prompt' for single string, 'messages' for chat-style",
    )
    parser.add_argument(
        "--prompt_multiplier",
        type=int,
        default=1,
        help="Number of times to repeat each prompt",
    )

    args = parser.parse_args()

    if args.duration is not None:
        if len(args.concurrency) != 1:
            parser.error(
                "When using --duration, specify exactly one --concurrency value."
            )

    # Ensure num_prompts and concurrency have matching lengths or handle appropriately
    if args.concurrency is not None:
        if len(args.num_prompts) == 1 and len(args.concurrency) > 1:
            # If only one num_prompts value is provided, duplicate it for each concurrency
            args.num_prompts = args.num_prompts * len(args.concurrency)
        elif len(args.num_prompts) != len(args.concurrency):
            parser.error(
                f"Number of --num_prompts values ({len(args.num_prompts)}) must match "
                f"number of --concurrency values ({len(args.concurrency)})."
            )

    # Parse extra_request_body if provided
    if args.extra_request_body:
        try:
            args.extra_request_body = json.loads(args.extra_request_body)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format for --extra_request_body")
    else:
        args.extra_request_body = {}

    # Ensure input_file is provided if input_type is 'file'
    if args.input_type == "file" and not args.input_file:
        parser.error("--input_file is required when --input_type is 'file'")

    # Set default output filename if not provided
    if not args.output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output_file = f"benchmark_{timestamp}.csv"
    elif not args.output_file.endswith(".csv"):
        args.output_file += ".csv"

    if args.concurrency is None and args.request_rate is None:
        parser.error("At least one of --concurrency or --request_rate must be provided")

    if args.concurrency is None:
        args.concurrency = [
            float("inf")
        ]  # Use infinite concurrency for rate-limited benchmarks

    if args.request_rate is None:
        args.request_rate = float("inf")
    return args
