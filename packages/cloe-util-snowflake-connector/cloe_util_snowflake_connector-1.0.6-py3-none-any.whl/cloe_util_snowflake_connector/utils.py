from enum import Enum

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


class PrivateKeyHeaderFooter(Enum):
    """
    An enumeration of PEM headers and footers for private keys in PKCS#8 format.

    Attributes:
        PKCS8_UNENCRYPTED_HEADER (str): The header for an unencrypted private key in PKCS#8 format.
        PKCS8_UNENCRYPTED_FOOTER (str): The footer for an unencrypted private key in PKCS#8 format.
        PKCS8_ENCRYPTED_HEADER (str): The header for an encrypted private key in PKCS#8 format.
        PKCS8_ENCRYPTED_FOOTER (str): The footer for an encrypted private key in PKCS#8 format.
    """

    PKCS8_UNENCRYPTED_HEADER = """-----BEGIN PRIVATE KEY-----"""
    PKCS8_UNENCRYPTED_FOOTER = """-----END PRIVATE KEY-----"""
    PKCS8_ENCRYPTED_HEADER = """-----BEGIN ENCRYPTED PRIVATE KEY-----"""
    PKCS8_ENCRYPTED_FOOTER = """-----END ENCRYPTED PRIVATE KEY-----"""


def encode_to_binary_der(private_key: str, passphrase: bytes | None) -> bytes:
    """
    Converts a PEM-encoded private key into its binary (DER) format.

    Args:
        private_key (str): The PEM-encoded private key as a string.
        passphrase (bytes | None): The passphrase to decrypt the private key,
                                    or None if the key is not encrypted.

    Returns:
        bytes: The private key in binary (DER) format.

    Raises:
        ValueError: If the private key cannot be loaded or is invalid.
    """
    p_key = serialization.load_pem_private_key(
        private_key.encode("utf-8"), password=passphrase, backend=default_backend()
    )

    pkb = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return pkb


def transform_to_pem(private_key: str, private_key_header_footer=PrivateKeyHeaderFooter, encoded=True) -> str:
    """
    Transforms a base64-encoded private key into PEM format by adding the appropriate header and footer.

    Args:
        private_key (str): The base64-encoded private key as a string.

    Returns:
        str: The private key in PEM format with the header and footer added.

    Example:
        Input: "MIIBVgIBADANBgkqhkiG9w0BAQEFAASCATIwggEuAgEAAkEA..."
        Output:
        "-----BEGIN PRIVATE KEY-----
        MIIBVgIBADANBgkqhkiG9w0BAQEFAASCATIwggEuAgEAAkEA...
        -----END PRIVATE KEY-----"
    """
    if encoded and private_key.startswith("\n") and private_key.endswith("\n"):
        private_key_pem = f"""{private_key_header_footer.PKCS8_ENCRYPTED_HEADER.value}{private_key}{private_key_header_footer.PKCS8_ENCRYPTED_FOOTER.value}"""
    elif encoded and not private_key.startswith("\n") and not private_key.endswith("\n"):
        private_key_pem = f"""{private_key_header_footer.PKCS8_ENCRYPTED_HEADER.value}\n{private_key}\n{private_key_header_footer.PKCS8_ENCRYPTED_FOOTER.value}"""
    elif not encoded and private_key.startswith("\n") and private_key.endswith("\n"):
        private_key_pem = f"""{private_key_header_footer.PKCS8_UNENCRYPTED_HEADER.value}{private_key}{private_key_header_footer.PKCS8_UNENCRYPTED_FOOTER.value}"""
    elif not encoded and not private_key.startswith("\n") and not private_key.endswith("\n"):
        private_key_pem = f"""{private_key_header_footer.PKCS8_UNENCRYPTED_HEADER.value}\n{private_key}\n{private_key_header_footer.PKCS8_UNENCRYPTED_FOOTER.value}"""

    return private_key_pem


def add_line_breaks(input_string: str, line_length=64) -> str:
    """
    Adds a line break after every 'line_length' characters in the input string.

    Args:
        input_string (str): The string to format.
        line_length (int): The number of characters per line (default is 64).

    Returns:
        str: The formatted string with line breaks.
    """
    return "\n".join(input_string[i : i + line_length] for i in range(0, len(input_string), line_length))


def modify_private_keys(
    private_key: str,
    passphrase: bytes | None,
    line_breaks_replacement: bool,
    convert_to_pem: bool,
    insert_line_breaks: bool,
    replace_header_footer: bool,
    encoded: bool,
    private_key_header_footer=PrivateKeyHeaderFooter,
) -> bytes:
    """
    Modifies a private key based on the specified transformation options.

    This function allows for various manipulations of a private key, including:
    - Replacing line breaks (`\\n`) with actual newlines.
    - Converting the private key to PEM format.
    - Adding line breaks for readability.
    - Replacing or removing PEM headers and footers.

    Args:
        private_key (str): The private key string to modify.
        passphrase (bytes | None): The passphrase for the private key. If provided, the key is treated as encrypted.
        line_breaks_replacement (bool): If `True`, replaces `\\n` with newline characters.
        convert_to_pem (bool): If `True`, converts the private key to PEM format.
        insert_line_breaks (bool): If `True`, adds line breaks to the private key for readability.
        replace_header_footer (bool): If `True`, replaces or removes PEM headers and footers based on encryption.
        private_key_header_footer (Enum): The enumeration of PEM headers and footers. Defaults to `PrivateKeyHeaderFooter`.

    Returns:
        bytes: The modified private key in DER-encoded binary format.

    Raises:
        ValueError: If the private key is invalid or incompatible with the specified transformations.

    """

    if replace_header_footer:
        if passphrase is None:
            private_key = private_key.replace(private_key_header_footer.PKCS8_UNENCRYPTED_HEADER.value, "").replace(
                private_key_header_footer.PKCS8_UNENCRYPTED_FOOTER.value, ""
            )
        else:
            private_key = private_key.replace(private_key_header_footer.PKCS8_ENCRYPTED_HEADER.value, "").replace(
                private_key_header_footer.PKCS8_ENCRYPTED_FOOTER.value, ""
            )

    if line_breaks_replacement:
        line_breaks = "\\n"
        private_key = private_key.replace(line_breaks, "\n")

    if insert_line_breaks:
        private_key = add_line_breaks(input_string=private_key)

    if convert_to_pem:
        private_key = transform_to_pem(private_key=private_key, encoded=encoded)

    modified_private_key = encode_to_binary_der(private_key=private_key, passphrase=passphrase)

    return modified_private_key
