#!/usr/bin/env python3
"""
Awesome Chain - Simple Entry Point

A simple entry point for quick access to the framework.
Run this file to start in interactive mode.

Usage: python run.py [options]
        --react  Force ReAct mode (recommended for GLM/Qwen models)
        --model  Specify model name
"""

import sys
sys.path.insert(0, '.')

from cli import main


if __name__ == "__main__":
    main()
