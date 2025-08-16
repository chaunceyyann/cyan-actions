#!/usr/bin/env python3
"""
Shared logging configuration for report generators.
"""

import logging
import sys


def setup_logging(level=logging.DEBUG):
    """Setup logging with GitHub Actions format."""
    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    return logging.getLogger(__name__)


def get_logger(name):
    """Get a logger instance with the given name."""
    return logging.getLogger(name)
