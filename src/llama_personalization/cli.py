#!/usr/bin/env python3
"""
Command-line interface for llama_personalization.
"""

import argparse
import json
import logging
import sys
from typing import Dict, Any

# Use the client, not the engine directly
from llama_personalization.core import PersonalizationClient

logger = logging.getLogger("llama_personalization.cli")

def setup_logging(log_level_str: str = "INFO") -> None:
    """Set up logging configuration."""
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    # Configure root logger for the package
    pkg_logger = logging.getLogger("llama_personalization")
    pkg_logger.setLevel(log_level)
    if not pkg_logger.hasHandlers():
         handler = logging.StreamHandler(sys.stdout)
         formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
         handler.setFormatter(formatter)
         pkg_logger.addHandler(handler)
         pkg_logger.propagate = False # Prevent duplication if root logger also gets configured


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Llama Personalization Client CLI")

    # Removed --config argument for now
    parser.add_argument(
        "-l", "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run", required=True)

    # Get Recommendations command
    rec_parser = subparsers.add_parser("get-recommendations", help="Get personalized recommendations for a user.")
    rec_parser.add_argument("-u", "--user-id", required=True, help="The ID of the user.")
    rec_parser.add_argument("-c", "--context", type=json.loads, default={}, help='Contextual information as a JSON string (e.g., '{"page": "home"}').')
    rec_parser.add_argument("-n", "--num-recs", type=int, default=10, help="Number of recommendations to retrieve.")

    # Update Profile command
    update_parser = subparsers.add_parser("update-profile", help="Update a user's profile.")
    update_parser.add_argument("-u", "--user-id", required=True, help="The ID of the user whose profile to update.")
    update_parser.add_argument("-d", "--data", type=json.loads, required=True, help='Profile data as a JSON string (e.g., '{"interests": ["ai", "python"]}').')

    # Removed train, simulate, explain, export, delete commands

    return parser.parse_args()

def run_get_recommendations(args: argparse.Namespace, client: PersonalizationClient) -> None:
    """Run the get-recommendations command."""
    logger.info(f"Requesting recommendations for user: {args.user_id}")
    try:
        recommendations = client.get_recommendations(
            user_id=args.user_id,
            context=args.context,
            num_recommendations=args.num_recs
        )
        print(json.dumps(recommendations, indent=2))
        if recommendations.get("error"):
            sys.exit(1) # Exit with error if the client reported one
    except Exception as e:
        logger.error(f"Failed to get recommendations: {e}", exc_info=True)
        print(json.dumps({"error": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)

def run_update_profile(args: argparse.Namespace, client: PersonalizationClient) -> None:
    """Run the update-profile command."""
    logger.info(f"Requesting profile update for user: {args.user_id}")
    
    # Ensure user_id from arg matches data if present, or add it
    profile_data = args.data
    if "user_id" in profile_data and profile_data["user_id"] != args.user_id:
        logger.error(f"User ID mismatch: Argument '{args.user_id}' does not match ID in data '{profile_data['user_id']}'.")
        sys.exit(1)
    elif "user_id" not in profile_data:
         profile_data["user_id"] = args.user_id
    
    try:
        result = client.update_profile(profile_data=profile_data)
        print(json.dumps(result, indent=2))
        if not result.get("success"):
            sys.exit(1) # Exit with error if the client reported failure
    except Exception as e:
        logger.error(f"Failed to update profile: {e}", exc_info=True)
        print(json.dumps({"error": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)

def main() -> None:
    """Main entry point for the CLI."""
    args = parse_args()
    setup_logging(args.log_level)

    # Initialize the client (using default config for now)
    # TODO: Potentially allow config overrides via CLI flags or env vars if needed later
    client = PersonalizationClient()

    # Run the appropriate command
    if args.command == "get-recommendations":
        run_get_recommendations(args, client)
    elif args.command == "update-profile":
        run_update_profile(args, client)
    else:
        # Should not happen due to `required=True` in add_subparsers
        logger.error(f"Unknown command: {args.command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
