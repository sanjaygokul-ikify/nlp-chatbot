"""
utils.py — Utility helpers for NLP Chatbot.

PEP 8 compliant. Keep concise and readable.
"""

import logging

# Configure root logger once at module level
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def log_message(message: str) -> None:
    """Log an informational message."""
    logger.info(message)
