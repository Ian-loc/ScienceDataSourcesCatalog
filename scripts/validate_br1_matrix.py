#!/usr/bin/env python3
"""Compatibilidade: valida somente o lote BR1 pelo validador comum."""
from validate_br_batches import validate_batches


if __name__ == "__main__":
    validate_batches("BR1")
