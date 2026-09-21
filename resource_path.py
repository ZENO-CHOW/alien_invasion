"""Resolve bundled game resources independently of the working directory."""

from pathlib import Path
import sys


def resource_path(*parts: str) -> Path:
    """Return a resource path for source runs and PyInstaller bundles."""
    bundle_dir = getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
    return Path(bundle_dir).joinpath(*parts)
