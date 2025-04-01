"""
Unicode Metadata Embedding Utility for EncypherAI

This module provides utilities for embedding metadata (model info, timestamps)
into text using Unicode variation selectors without affecting readability.
"""

import re
import json
import hmac
import hashlib
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union, Any
import zlib


class MetadataTarget(Enum):
    """Enum for specifying where to embed metadata in text"""

    WHITESPACE = "whitespace"  # Default - embed in whitespace
    PUNCTUATION = "punctuation"  # Embed in punctuation marks
    FIRST_LETTER = "first_letter"  # Embed in first letter of each word
    LAST_LETTER = "last_letter"  # Embed in last letter of each word
    ALL_CHARACTERS = "all_characters"  # Embed in all characters (not recommended)
    NONE = "none"  # Don't embed metadata (for testing/debugging)


class UnicodeMetadata:
    """Utility class for embedding and extracting metadata using Unicode variation selectors"""

    # Variation selectors block (VS1-VS16: U+FE00 to U+FE0F)
    VARIATION_SELECTOR_START = 0xFE00
    VARIATION_SELECTOR_END = 0xFE0F

    # Variation selectors supplement (VS17-VS256: U+E0100 to U+E01EF)
    VARIATION_SELECTOR_SUPPLEMENT_START = 0xE0100
    VARIATION_SELECTOR_SUPPLEMENT_END = 0xE01EF

    # Regular expressions for different target types
    REGEX_PATTERNS = {
        MetadataTarget.WHITESPACE: re.compile(r"(\s)"),
        MetadataTarget.PUNCTUATION: re.compile(r"([.,!?;:])"),
        MetadataTarget.FIRST_LETTER: re.compile(r"(\b\w)"),
        MetadataTarget.LAST_LETTER: re.compile(r"(\w\b)"),
        MetadataTarget.ALL_CHARACTERS: re.compile(r"(.)"),
    }

    @classmethod
    def to_variation_selector(cls, byte: int) -> Optional[str]:
        """
        Convert a byte to a variation selector character

        Args:
            byte: Byte value (0-255)

        Returns:
            Unicode variation selector character or None if byte is out of range
        """
        if 0 <= byte < 16:
            return chr(cls.VARIATION_SELECTOR_START + byte)
        elif 16 <= byte < 256:
            return chr(cls.VARIATION_SELECTOR_SUPPLEMENT_START + byte - 16)
        else:
            return None

    @classmethod
    def from_variation_selector(cls, code_point: int) -> Optional[int]:
        """
        Convert a variation selector code point to a byte

        Args:
            code_point: Unicode code point

        Returns:
            Byte value (0-255) or None if not a variation selector
        """
        if cls.VARIATION_SELECTOR_START <= code_point <= cls.VARIATION_SELECTOR_END:
            return code_point - cls.VARIATION_SELECTOR_START
        elif (
            cls.VARIATION_SELECTOR_SUPPLEMENT_START
            <= code_point
            <= cls.VARIATION_SELECTOR_SUPPLEMENT_END
        ):
            return (code_point - cls.VARIATION_SELECTOR_SUPPLEMENT_START) + 16
        else:
            return None

    @classmethod
    def encode(cls, emoji: str, text: str) -> str:
        """
        Encode text into an emoji using Unicode variation selectors

        Args:
            emoji: Base character to encode the text into
            text: Text to encode

        Returns:
            Encoded string with the text hidden in variation selectors
        """
        # Convert the string to UTF-8 bytes
        bytes_data = text.encode("utf-8")

        # Start with the emoji
        encoded = emoji

        # Add variation selectors for each byte
        for byte in bytes_data:
            vs = cls.to_variation_selector(byte)
            if vs:
                encoded += vs

        return encoded

    @classmethod
    def decode(cls, text: str) -> str:
        """
        Decode text from Unicode variation selectors

        Args:
            text: Text with embedded variation selectors

        Returns:
            Decoded text
        """
        # Extract bytes from variation selectors
        decoded: List[int] = []

        for char in text:
            code_point = ord(char)
            byte = cls.from_variation_selector(code_point)

            # If we've found a non-variation selector after we've started collecting bytes,
            # we're done
            if byte is None and len(decoded) > 0:
                break
            # If it's not a variation selector and we haven't started collecting bytes yet,
            # it's probably the base character (emoji), so skip it
            elif byte is None:
                continue

            decoded.append(byte)

        # Convert bytes back to text
        if decoded:
            return bytes(decoded).decode("utf-8")
        else:
            return ""

    @classmethod
    def extract_bytes(cls, text: str) -> bytes:
        """
        Extract bytes from Unicode variation selectors

        Args:
            text: Text with embedded variation selectors

        Returns:
            Bytes extracted from variation selectors
        """
        # Extract bytes from variation selectors
        decoded: List[int] = []

        for char in text:
            code_point = ord(char)
            byte = cls.from_variation_selector(code_point)

            # If we've found a non-variation selector after we've started collecting bytes,
            # we're done
            if byte is None and len(decoded) > 0:
                break
            # If it's not a variation selector and we haven't started collecting bytes yet,
            # it's probably the base character (emoji), so skip it
            elif byte is None:
                continue

            decoded.append(byte)

        # Convert bytes back to bytes object
        if decoded:
            return bytes(decoded)
        else:
            return b""

    @classmethod
    def embed_metadata(
        cls,
        text: str,
        model_id: Optional[str] = None,
        timestamp: Optional[Union[str, datetime, int, float]] = None,
        target: Optional[Union[str, MetadataTarget]] = None,
        custom_metadata: Optional[Dict[str, Any]] = None,
        hmac_secret_key: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """
        Embed model and timestamp metadata into text using Unicode variation selectors.

        Args:
            text: The text to embed metadata into
            model_id: The model ID to embed
            timestamp: The timestamp to embed (can be a string, datetime object, or Unix timestamp)
            target: Where to embed the metadata (whitespace, punctuation, first_letter, last_letter, all_characters)
            custom_metadata: Additional custom metadata to embed
            hmac_secret_key: Optional secret key for HMAC verification
            **kwargs: Additional metadata fields to include

        Returns:
            Text with embedded metadata
        """
        if not text:
            return text

        # Create metadata dictionary
        metadata: Dict[str, Union[str, int, float, Any]] = {
            "model_id": model_id or "",
        }

        # Handle timestamp with proper type checking
        if timestamp is None:
            # Use current time as Unix timestamp
            metadata["timestamp"] = int(datetime.now(timezone.utc).timestamp())
        elif isinstance(timestamp, str):
            try:
                # Try to parse string as ISO format and convert to Unix timestamp
                dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                metadata["timestamp"] = int(dt.timestamp())
            except ValueError:
                # If parsing fails, store as is
                metadata["timestamp"] = timestamp
        elif isinstance(timestamp, datetime):
            # Convert datetime to Unix timestamp
            metadata["timestamp"] = int(timestamp.timestamp())
        elif isinstance(timestamp, (int, float)):
            # Already a Unix timestamp, store as is
            metadata["timestamp"] = int(timestamp)
        else:
            # Fallback for any other type
            metadata["timestamp"] = str(timestamp)

        # Add custom metadata if provided
        if custom_metadata:
            metadata.update(custom_metadata)

        # Add any additional kwargs as metadata
        if kwargs:
            metadata.update(kwargs)

        # Convert metadata to JSON string
        json_str = json.dumps(metadata, separators=(",", ":"))

        # Add HMAC if secret key is provided
        if hmac_secret_key:
            # Create HMAC signature
            signature = hmac.new(
                hmac_secret_key.encode("utf-8"),
                json_str.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()

            # Add signature to metadata
            json_str = json.dumps(
                {"data": metadata, "signature": signature}, separators=(",", ":")
            )

        # Map string target to enum value if needed
        if isinstance(target, str):
            try:
                # Try to map the string to an enum value
                target_enum = MetadataTarget(target)
            except ValueError:
                # Default to whitespace if the target string is not a valid enum value
                target_enum = MetadataTarget.WHITESPACE
        else:
            # If target is None or already an enum, use whitespace as default
            target_enum = (
                target
                if isinstance(target, MetadataTarget)
                else MetadataTarget.WHITESPACE
            )

        # If target is NONE, return the original text
        if target_enum == MetadataTarget.NONE:
            return text

        # Get the appropriate regex pattern
        pattern = cls.REGEX_PATTERNS.get(
            target_enum, cls.REGEX_PATTERNS[MetadataTarget.WHITESPACE]
        )

        # Find all matches in the text
        matches = list(pattern.finditer(text))
        if not matches:
            return text  # No places to embed metadata

        # Split the text into parts
        result = []
        last_end = 0

        # Encode metadata into all matching characters
        for match in matches:
            # Add text before the match
            result.append(text[last_end : match.start()])

            # Get the character to embed metadata into
            char = match.group(1)

            # Encode the metadata into the character
            result.append(cls.encode(char, json_str))

            # Update last_end for next iteration
            last_end = match.end()

        # Add the remaining text after the last match
        result.append(text[last_end:])

        return "".join(result)

    @classmethod
    def extract_metadata(cls, text: str) -> Dict[str, Any]:
        """
        Extract metadata from text with embedded Unicode variation selectors.

        Args:
            text: Text with embedded metadata

        Returns:
            Dictionary containing the extracted metadata
        """
        # Extract bytes from text
        data_bytes = cls.extract_bytes(text)
        if not data_bytes:
            return {"model_id": "", "timestamp": None}

        try:
            # Parse JSON
            try:
                # Check if this is HMAC-signed metadata (has data and signature fields)
                parsed_json = json.loads(data_bytes.decode("utf-8"))
                if (
                    isinstance(parsed_json, dict)
                    and "data" in parsed_json
                    and "signature" in parsed_json
                ):
                    # This is signed data, extract just the data portion
                    metadata: Dict[str, Any] = parsed_json["data"]
                else:
                    # Regular metadata
                    metadata = parsed_json

                # Ensure model_id has a default empty string if not present
                if "model_id" not in metadata:
                    metadata["model_id"] = ""

                # Handle timestamp conversion if present
                if "timestamp" in metadata:
                    if isinstance(metadata["timestamp"], (int, float)):
                        # Convert Unix timestamp to datetime
                        metadata["timestamp"] = datetime.fromtimestamp(
                            metadata["timestamp"], tz=timezone.utc
                        )
                    elif isinstance(metadata["timestamp"], str):
                        # Try to parse ISO format
                        try:
                            metadata["timestamp"] = datetime.fromisoformat(
                                metadata["timestamp"].replace("Z", "+00:00")
                            )
                        except ValueError:
                            # If parsing fails, leave as is
                            pass

                return metadata
            except json.JSONDecodeError:
                return {"model_id": "", "timestamp": None}
        except Exception:
            return {"model_id": "", "timestamp": None}

    @classmethod
    def verify_metadata(
        cls, text: str, hmac_secret_key: str
    ) -> Tuple[Dict[str, Any], bool]:
        """
        Verify and extract metadata from text with HMAC verification.

        Args:
            text: Text with embedded metadata
            hmac_secret_key: Secret key used for HMAC verification

        Returns:
            Tuple of (metadata, is_verified) where is_verified is True if
            the HMAC signature is valid
        """
        if not hmac_secret_key:
            return cls.extract_metadata(text), False

        # Extract bytes from text
        raw_metadata = cls.extract_bytes(text)
        if not raw_metadata:
            return {"model_id": "", "timestamp": None}, False

        try:
            parsed_json = json.loads(raw_metadata.decode("utf-8"))

            # Check if this is HMAC-signed metadata
            if (
                isinstance(parsed_json, dict)
                and "data" in parsed_json
                and "signature" in parsed_json
            ):
                data = parsed_json["data"]
                signature = parsed_json["signature"]

                # Verify the signature
                data_json = json.dumps(data, separators=(",", ":"))
                expected_signature = hmac.new(
                    hmac_secret_key.encode("utf-8"),
                    data_json.encode("utf-8"),
                    hashlib.sha256,
                ).hexdigest()

                # Compare signatures
                is_verified = hmac.compare_digest(signature, expected_signature)

                # Process the metadata (same as in extract_metadata)
                metadata = data

                # Ensure model_id has a default empty string if not present
                if "model_id" not in metadata:
                    metadata["model_id"] = ""

                # Handle timestamp conversion if present
                if "timestamp" in metadata:
                    if isinstance(metadata["timestamp"], (int, float)):
                        metadata["timestamp"] = datetime.fromtimestamp(
                            metadata["timestamp"], tz=timezone.utc
                        )
                    elif isinstance(metadata["timestamp"], str):
                        try:
                            metadata["timestamp"] = datetime.fromisoformat(
                                metadata["timestamp"].replace("Z", "+00:00")
                            )
                        except ValueError:
                            # If parsing fails, leave as is
                            pass

                return metadata, is_verified
            else:
                # Not signed data, return the metadata but verification is False
                return cls.extract_metadata(text), False

        except (json.JSONDecodeError, KeyError, TypeError):
            # If any error occurs during parsing, return empty metadata and False
            return {"model_id": "", "timestamp": None}, False
