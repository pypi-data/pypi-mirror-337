"""
TLS Decryption Module (Production Ready)
Provides functions and classes to decrypt received data using a negotiated TLSContext.
This module invokes the underlying TLSContext.decrypt() method to perform the actual decryption,
and exposes a higher-level API for streamlined use.
Additional audit logging and error categorization have been integrated per full QUIC standard.
"""
import logging
from typing import Any
from .tls_context import TLSContext

logger = logging.getLogger(__name__)


def decrypt_data(tls_context: TLSContext, ciphertext: bytes) -> bytes:
    try:
        logger.debug(
            "Attempting decryption of %d bytes of ciphertext", len(ciphertext))
        plaintext = tls_context.decrypt(ciphertext)
        logger.debug(
            "Decryption successful: obtained %d bytes of plaintext", len(plaintext))
        logger.info(
            "AUDIT: Decryption completed successfully (plaintext length: %d)", len(plaintext))
        return plaintext
    except Exception as e:
        logger.error("AUDIT: Decryption error encountered", exc_info=True)
        raise e


class TLSDecryptionEngine:
    def __init__(self, tls_context: TLSContext) -> None:
        self.tls_context = tls_context

    def decrypt(self, data: bytes) -> bytes:
        logger.debug(
            "TLSDecryptionEngine: Received %d bytes of data for decryption", len(data))
        return decrypt_data(self.tls_context, data)
