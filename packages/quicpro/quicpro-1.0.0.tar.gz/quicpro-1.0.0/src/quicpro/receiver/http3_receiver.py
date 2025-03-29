#!/usr/bin/env python
"""
HTTP3 Receiver Module
This module implements an HTTP3Receiver that extracts, decodes, and validates
HTTP/3 frames from incoming QUIC packets and then forwards the decoded message
to a downstream decoder.
For demo purposes, the header block is assumed to be prefixed with a 2-byte big-endian length.
If a custom _decode_frame method is provided, its output is used; otherwise the entire
extracted frame is passed to the downstream decoder.
"""
import logging
from quicpro.exceptions import HTTP3FrameError

logger = logging.getLogger(__name__)


class HTTP3Receiver:
    """HTTP3Receiver processes incoming QUIC packets and decodes HTTP/3 frames."""
    
    def __init__(self, decoder: object) -> None:
        """
        Initialize the HTTP3Receiver.
        Args:
            decoder (object): An object with a consume(message: str) method.
        """
        self.decoder = decoder

    def receive(self, quic_packet: bytes) -> None:
        """Receives a QUIC packet and processes it to extract and decode the HTTP/3 frame."""
        try:
            logger.debug(
                "HTTP3Receiver received packet of length %d", len(quic_packet))
            frame = self._extract_http3_frame(quic_packet)
            if not self._validate_frame(frame):
                raise HTTP3FrameError(
                    "Extracted HTTP/3 frame failed validation.")
            logger.info("HTTP3Receiver successfully decoded frame")
            if hasattr(self, "_decode_frame"):
                header_block, _ = self._decode_frame(frame)
            else:
                header_block = frame
            try:
                message = header_block.decode("utf-8")
            except UnicodeDecodeError:
                message = "Unknown"
            self.decoder.consume(message)
        except HTTP3FrameError as exc:
            logger.exception("HTTP3Receiver processing failed", exc_info=exc)
            raise
        except Exception as exc:
            logger.exception("Unexpected error during processing", exc_info=exc)
            raise

    def _extract_http3_frame(self, packet: bytes) -> bytes:
        """Extracts the HTTP/3 frame from the incoming packet."""
        if not packet:
            raise HTTP3FrameError("Empty packet received.")
        if len(packet) >= 2:
            length = int.from_bytes(packet[:2], byteorder="big")
            if len(packet) >= 2 + length:
                return packet[2:2 + length]
        return packet

    def _validate_frame(self, frame: bytes) -> bool:
        """Validates the extracted HTTP/3 frame."""
        return len(frame) > 0

