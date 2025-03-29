import ast
import re
from pathlib import Path

import typing_extensions
from pydantic import BaseModel, computed_field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .utils import (
    PrivateKeyHeaderFooter,
    modify_private_keys,
)


class SessionParameters(BaseModel):
    query_tag: str


class EnvVariablesInitializer(BaseSettings):
    """
    A class for sourcing and initializing environment variables.

    This class utilizes Pydantic's `BaseSettings` to load environment variables and values
    from a `.env` file. Environment variables take precedence over values in the `.env` file.

    Configuration:
        - `env_prefix`: Prefix for environment variables (e.g., "CLOE_SNOWFLAKE_").
        - `env_file`: Path to the `.env` file.
        - `env_file_encoding`: Encoding used for reading the `.env` file.

    Attributes:
        user (str):
            The username for the connection.
        password (str | None):
            The password associated with the user. Optional.
        private_key (str | None):
            The private key as a string. Optional.
        private_key_passphrase (str | None):
            The passphrase for the private key, if applicable. Optional.
        private_key_file (str | None):
            The path to the private key file. Optional.
        private_key_file_pwd (str | None):
            The password for the private key file. Optional.
        account (str):
            The account identifier for the connection.
        warehouse (str | None):
            The warehouse to use for the session. Optional.
        database (str | None):
            The database to use for the session. Optional.
        schema (str | None):
            The database schema to use for the session. Optional.
        role (str | None):
            The role to assume for the session. Optional.
        autocommit (str | None):
            Whether autocommit is enabled. Optional.
    """

    model_config = SettingsConfigDict(
        env_prefix="CLOE_SNOWFLAKE_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    user: str
    password: str | None = None
    private_key: str | None = None
    private_key_passphrase: str | None = None
    private_key_file: str | None = None
    private_key_file_pwd: str | None = None
    account: str
    warehouse: str | None = None
    database: str | None = None
    schema: str | None = None  # type: ignore
    role: str | None
    autocommit: str | None = None

    @computed_field  # type: ignore[misc]
    @property
    def private_key_has_line_breaks(self) -> bool | None:
        """
        Checks if the private key contains line breaks.

        Returns:
            bool | None:
                - True if the private key contains "\\n".
                - False if the private key does not contain "\\n".
                - None if the private key is not set.
        """
        if self.private_key:
            return True if "\\n" in self.private_key else False
        else:
            return None

    @computed_field  # type: ignore[misc]
    @property
    def private_key_is_unencrypted(self) -> bool | None:
        """
        Determines if the private key is unencrypted.

        Returns:
            bool | None:
                - True if the private key contains the unencrypted PKCS#8 header and footer.
                - False if the private key does not contain the unencrypted PKCS#8 header and footer.
                - None if the private key is not set.
        """
        if self.private_key:
            return (
                True
                if PrivateKeyHeaderFooter.PKCS8_UNENCRYPTED_HEADER.value in self.private_key
                and PrivateKeyHeaderFooter.PKCS8_UNENCRYPTED_FOOTER.value in self.private_key
                else False
            )
        else:
            return None

    @computed_field  # type: ignore[misc]
    @property
    def private_key_is_encrypted(self) -> bool | None:
        """
        Determines if the private key is encrypted.

        Returns:
            bool | None:
                - True if the private key contains the encrypted PKCS#8 header and footer.
                - False if the private key does not contain the encrypted PKCS#8 header and footer.
                - None if the private key is not set.
        """
        if self.private_key:
            return (
                True
                if PrivateKeyHeaderFooter.PKCS8_ENCRYPTED_HEADER.value in self.private_key
                and PrivateKeyHeaderFooter.PKCS8_ENCRYPTED_FOOTER.value in self.private_key
                else False
            )
        else:
            return None

    @computed_field  # type: ignore[misc]
    @property
    def private_key_has_private_key_passphrase(self) -> bool | None:
        """
        Checks if the private key has a passphrase.

        Returns:
            bool | None:
                - True if a private key passphrase is provided.
                - False if no private key passphrase is provided.
                - None if the private key is not set.
        """
        if self.private_key:
            return True if self.private_key_passphrase is not None else False
        else:
            return None

    @computed_field  # type: ignore[misc]
    @property
    def private_key_is_encoded(self) -> bool | None:
        """
        Determines if the private key is encoded.

        Note: If no headers/footers are provided, and a passphrase is supplied,
        it assumes the private key is encoded.

        Returns:
            bool | None:
                - True if the private key is determined to be encoded.
                - False if the private key is determined not to be encoded.
                - None if the private key is not set.
        """

        # problem: if no header/footers are provided it is not possible to check if key is
        # encrypted or not, in this case the assumption is that a provided passphrase is used to determine if
        # private_key is encrypted or not
        if self.private_key:
            if (
                not self.private_key_is_encrypted
                and not self.private_key_is_unencrypted
                and self.private_key_has_private_key_passphrase
            ):
                is_encoded = True
            elif (
                not self.private_key_is_encrypted
                and not self.private_key_is_unencrypted
                and not self.private_key_has_private_key_passphrase
            ):
                is_encoded = False
            elif self.private_key_is_encrypted and self.private_key_has_private_key_passphrase:
                is_encoded = True
            else:
                is_encoded = False
            return is_encoded
        else:
            return None

    @computed_field  # type: ignore[misc]
    @property
    def private_key_lacks_headers_footers(self) -> bool | None:
        """
        Checks if the private key lacks headers or footers.

        Returns:
            bool | None:
                - True if no valid headers or footers are found in the private key.
                - False if valid headers or footers are found in the private key.
                - None if the private key is not set.
        """
        if self.private_key:
            lacks_headers = not any(header.value in self.private_key for header in PrivateKeyHeaderFooter)
            return lacks_headers
        else:
            return None

    @computed_field  # type: ignore[misc]
    @property
    def converted_private_key_passphrase(self) -> bytes | None:
        """
        Converts the private key passphrase to bytes.

        Returns:
            bytes | None:
                - The private key passphrase encoded in UTF-8 as bytes.
                - None if the private key or passphrase is not set.
        """
        if self.private_key and self.private_key_passphrase:
            return self.private_key_passphrase.encode("utf-8")
        else:
            return None


class PrivateKeyModificationOptions(BaseModel):
    """
    Represents options for modifying private keys.

    Attributes:
        passphrase (bytes | None):
            The passphrase for the private key, if applicable. Optional.
        line_breaks_replacement (bool):
            Indicates whether to replace existing line breaks in the private key.
        insert_line_breaks (bool):
            Specifies whether to insert line breaks into the private key.
        convert_to_pem (bool):
            Specifies whether to convert the private key to PEM format.
        replace_header_footer (bool):
            Indicates whether to replace the header and footer of the private key.
        encoded (bool):
            Indicates whether the private key is encoded.
    """

    passphrase: bytes | None
    line_breaks_replacement: bool
    insert_line_breaks: bool
    convert_to_pem: bool
    replace_header_footer: bool
    encoded: bool


class PrivateKeyCondition(BaseModel):
    """
    Represents the conditions related to a private key.

    Attributes:
        is_unencrypted (bool): Indicates if the private key is unencrypted.
        is_encrypted (bool): Indicates if the private key is encrypted.
        has_line_breaks (bool): Indicates if the private key contains line breaks.
        has_private_key_passphrase (bool): Indicates if the private key has an associated passphrase.
        lacks_headers_footers (bool): Indicates if the private key lacks valid headers or footers.
        is_encoded (bool): Indicates if the private key is encoded.
        private_key_modification_options (PrivateKeyModificationOptions):
            The available modification options for the private key based on its conditions.
    """

    is_unencrypted: bool
    is_encrypted: bool
    has_line_breaks: bool
    has_private_key_passphrase: bool
    lacks_headers_footers: bool
    is_encoded: bool
    private_key_modification_options: PrivateKeyModificationOptions


class PrivateKeyConditions(BaseModel):
    """
    Represents a collection of private key conditions and provides functionality to match conditions.

    Attributes:
        private_key_conditions (list[PrivateKeyCondition]):
            A list of `PrivateKeyCondition` objects representing different private key states.
    """

    private_key_conditions: list[PrivateKeyCondition]

    def get_private_key_modification_option(
        self,
        is_unencrypted: bool | None,
        is_encrypted: bool | None,
        has_line_breaks: bool | None,
        has_private_key_passphrase: bool | None,
        lacks_headers_footers: bool | None,
        is_encoded: bool | None,
    ) -> PrivateKeyModificationOptions | None:
        """
        Retrieves the modification options for a private key based on the specified conditions.

        Args:
            is_unencrypted (bool | None): Indicates if the private key is unencrypted.
            is_encrypted (bool | None): Indicates if the private key is encrypted.
            has_line_breaks (bool | None): Indicates if the private key contains line breaks.
            has_private_key_passphrase (bool | None): Indicates if the private key has an associated passphrase.
            lacks_headers (bool | None): Indicates if the private key lacks valid headers or footers.
            is_encoded (bool | None): Indicates if the private key is encoded.

        Returns:
            PrivateKeyModificationOptions | None:
                The modification options for the matching private key condition.
                Returns `None` if no matching condition is found.
        """
        for private_key_condition in self.private_key_conditions:
            if (
                private_key_condition.is_unencrypted == is_unencrypted
                and private_key_condition.is_encrypted == is_encrypted
                and private_key_condition.has_line_breaks == has_line_breaks
                and private_key_condition.has_private_key_passphrase == has_private_key_passphrase
                and private_key_condition.lacks_headers_footers == lacks_headers_footers
                and private_key_condition.is_encoded == is_encoded
            ):
                return private_key_condition.private_key_modification_options
        return None


class ConnectionParameters(BaseModel):
    """
    Represents connection parameters and their attributes, ensuring values are normalized.

    Attributes:
        user (str):
            The username for the connection.
        password (str | None):
            The password associated with the user. Optional.
        private_key (bytes | None):
            The private key in bytes format. Optional.
        private_key_file (str | None):
            The path to the private key file. Optional.
        private_key_file_pwd (str | None):
            The password for the private key file, if applicable. Optional.
        account (str):
            The account identifier for the connection.
        warehouse (str | None):
            The warehouse to use for the session. Optional
        database (str | None):
            The database to use for the session. Optional.
        schema (str | None):
            The database schema to use for the session. Optional.
        role (str | None):
            The role to assume for the session. Optional.
        autocommit (bool | None):
            Whether to enable autocommit for the session. Defaults to True. Optional.
        session_parameters (SessionParameters | None):
            Additional session parameters for the connection. Optional.
    """

    user: str
    password: str | None = None
    private_key: bytes | None = None
    private_key_file: str | None = None
    private_key_file_pwd: str | None = None
    account: str
    warehouse: str | None = None
    database: str | None = None
    schema: str | None = None  # type: ignore
    role: str | None
    autocommit: bool | None = True
    session_parameters: SessionParameters | None = None

    @classmethod
    def init_from_env_variables(cls, env_file: Path = Path(".env")) -> typing_extensions.Self:
        """
        Initialize an instance of the class using environment variables.

        This method reads environment variables from the specified `.env` file,
        initializes an `EnvVariablesInitializer` object, and uses the parsed
        environment variables to create and return an instance of the class.

        see class EnvVariablesInitializer for more details

        Args:
            env_file (Path): The path to the `.env` file containing environment
                variables. Defaults to `.env` in the current working directory.

        Returns:
            typing_extensions.Self: An instance of the class initialized with
                values from the environment variables.
        """
        env_vars = EnvVariablesInitializer(_env_file=env_file)  # type: ignore
        return cls(**env_vars.model_dump())

    @field_validator("autocommit", mode="before")
    @classmethod
    def convert_to_bool(cls, v: str | bool) -> bool:
        """
        Converts the given autocommit value to a boolean.

        - If the input is a string ("True" or "False"), it is converted to a boolean using `ast.literal_eval`.
        - If the input is already a boolean, it is returned as-is.
        - Raises a `ValueError` if the string is not "True" or "False".

        Args:
            v (str | bool): The autocommit value as a string or boolean.

        Returns:
            bool: The converted boolean value.

        Raises:
            ValueError: If the input string is not "True" or "False".
        """
        if isinstance(v, str):
            if v in ["True", "False"]:
                return ast.literal_eval(v)
            else:
                raise ValueError("Passed autocommit values are not 'True' or 'False'")
        else:
            return v

    @field_validator("account", mode="before")
    @classmethod
    def clean_account_identifier(cls, v: str) -> str:
        """
        Cleans the account identifier by removing specific parts of the URL.

        - Removes the `.snowflakecomputing.com` domain and anything following it.
        - Strips the `https://` prefix from the account identifier.

        Args:
            v (str): The raw account identifier string, typically a full URL.

        Returns:
            str: The cleaned account identifier string with unnecessary parts removed.
        """
        return re.sub(r"\.snowflakecomputing\.com.*", "", v).replace("https://", "")

    @model_validator(mode="before")
    @classmethod
    def preprocess_private_key(cls, data: dict) -> dict:
        """
        Preprocesses a private key to convert it into a binary DER-encoded format.

        This method handles various formats and conditions for private keys, performing tasks such as:
        - Replacing escaped newline characters (`\\n`) with actual newlines when necessary.
        - Adding or replacing PEM headers and footers for keys that lack them.
        - Validating and transforming encrypted and unencrypted keys based on their characteristics and passphrase presence.

        The function uses predefined mappings between key conditions and modification options to apply transformations.

        Args:
            cls: The class context (used in class methods).
            data (dict): A dictionary containing private key data and associated metadata:
                - `private_key` (str): The private key as a string.
                - `private_key_passphrase` (str | None): An optional passphrase for encrypted keys.
                - `private_key_has_line_breaks` (bool | None): Whether the private key has line breaks.
                - `private_key_is_unencrypted` (bool | None): Whether the private key is unencrypted.
                - `private_key_is_encrypted` (bool | None): Whether the private key is encrypted.
                - `private_key_has_private_key_passphrase` (bool | None): Whether the key has a passphrase.
                - `private_key_lacks_headers_footers` (bool | None): Whether the private key lacks headers/footers.
                - `private_key_is_encoded` (bool | None): Whether the key is encoded.

        Returns:
            dict: The updated data dictionary, with the `private_key` transformed into a DER-encoded format.

        Raises:
            ValueError: If the private key format is invalid, unsupported, or a combination of unencrypted key with a passphrase is provided.

        Notes:
            - This method uses a mapping of conditions (via `PrivateKeyConditions`) to determine the appropriate modification options.
            - If no matching modification option is found for the given conditions, an exception is raised.
            - The function ensures that PEM headers, footers, and line breaks are properly handled to maintain a valid key format.

        Warnings:
            - If the private key is unencrypted but includes a passphrase, the method raises a `ValueError`.
            - The absence of matching modification options may indicate an invalid or unsupported private key format.
        """

        private_key = data.get("private_key")
        private_key_passphrase = data.get("converted_private_key_passphrase")

        if not private_key:
            return data

        has_line_breaks = data.get("private_key_has_line_breaks")
        is_unencrypted = data.get("private_key_is_unencrypted")
        is_encrypted = data.get("private_key_is_encrypted")
        has_private_key_passphrase = data.get("private_key_has_private_key_passphrase")
        is_encoded = data.get("private_key_has_private_key_passphrase")
        lacks_headers_footers = data.get("private_key_lacks_headers_footers")

        private_key_conditions_options_mapping = PrivateKeyConditions(
            private_key_conditions=[
                # mapping: Unencrypted key with headers/footers and line breaks
                PrivateKeyCondition(
                    is_unencrypted=True,
                    is_encrypted=False,
                    has_line_breaks=True,
                    has_private_key_passphrase=False,
                    lacks_headers_footers=False,
                    is_encoded=False,
                    private_key_modification_options=PrivateKeyModificationOptions(
                        passphrase=private_key_passphrase,
                        line_breaks_replacement=True,
                        insert_line_breaks=False,
                        convert_to_pem=False,
                        replace_header_footer=False,
                        encoded=False,
                    ),
                ),
                # mapping: Encrypted key with headers/footers and line breaks
                PrivateKeyCondition(
                    is_unencrypted=False,
                    is_encrypted=True,
                    has_line_breaks=True,
                    has_private_key_passphrase=True,
                    lacks_headers_footers=False,
                    is_encoded=True,
                    private_key_modification_options=PrivateKeyModificationOptions(
                        passphrase=private_key_passphrase,
                        line_breaks_replacement=True,
                        insert_line_breaks=False,
                        convert_to_pem=False,
                        replace_header_footer=False,
                        encoded=True,
                    ),
                ),
                # mapping: key without headers/footers and without line breaks and without passphrase, i.e. unencrypted private key
                PrivateKeyCondition(
                    is_unencrypted=False,
                    is_encrypted=False,
                    has_line_breaks=False,
                    has_private_key_passphrase=False,
                    lacks_headers_footers=True,
                    is_encoded=False,
                    private_key_modification_options=PrivateKeyModificationOptions(
                        passphrase=private_key_passphrase,
                        line_breaks_replacement=False,
                        insert_line_breaks=True,
                        convert_to_pem=True,
                        replace_header_footer=False,
                        encoded=False,
                    ),
                ),
                # mapping: key without headers/footers and without line breaks but with passphrase, i.e. encrypted private key
                PrivateKeyCondition(
                    is_unencrypted=False,
                    is_encrypted=False,
                    has_line_breaks=False,
                    has_private_key_passphrase=True,
                    lacks_headers_footers=True,
                    is_encoded=True,
                    private_key_modification_options=PrivateKeyModificationOptions(
                        passphrase=private_key_passphrase,
                        line_breaks_replacement=False,
                        insert_line_breaks=True,
                        convert_to_pem=True,
                        replace_header_footer=False,
                        encoded=True,
                    ),
                ),
                # mapping: Unencrypted key with headers/footers and no line breaks in key body
                PrivateKeyCondition(
                    is_unencrypted=True,
                    is_encrypted=False,
                    has_line_breaks=True,
                    has_private_key_passphrase=False,
                    lacks_headers_footers=False,
                    is_encoded=False,
                    private_key_modification_options=PrivateKeyModificationOptions(
                        passphrase=private_key_passphrase,
                        line_breaks_replacement=True,
                        insert_line_breaks=False,
                        convert_to_pem=False,
                        replace_header_footer=True,
                        encoded=False,
                    ),
                ),
                # mapping: Encrypted key with headers/footers and no line breaks in key body
                PrivateKeyCondition(
                    is_unencrypted=False,
                    is_encrypted=True,
                    has_line_breaks=True,
                    has_private_key_passphrase=True,
                    lacks_headers_footers=False,
                    is_encoded=True,
                    private_key_modification_options=PrivateKeyModificationOptions(
                        passphrase=private_key_passphrase,
                        line_breaks_replacement=True,
                        insert_line_breaks=False,
                        convert_to_pem=False,
                        replace_header_footer=True,
                        encoded=True,
                    ),
                ),
                # mapping: Unencrypted key with headers/footers and no line breaks
                PrivateKeyCondition(
                    is_unencrypted=True,
                    is_encrypted=False,
                    has_line_breaks=False,
                    has_private_key_passphrase=False,
                    lacks_headers_footers=False,
                    is_encoded=False,
                    private_key_modification_options=PrivateKeyModificationOptions(
                        passphrase=private_key_passphrase,
                        line_breaks_replacement=False,
                        insert_line_breaks=True,
                        convert_to_pem=True,
                        replace_header_footer=True,
                        encoded=False,
                    ),
                ),
                # mapping: Encrypted key with headers/footers and no line breaks
                PrivateKeyCondition(
                    is_unencrypted=False,
                    is_encrypted=True,
                    has_line_breaks=False,
                    has_private_key_passphrase=True,
                    lacks_headers_footers=False,
                    is_encoded=True,
                    private_key_modification_options=PrivateKeyModificationOptions(
                        passphrase=private_key_passphrase,
                        line_breaks_replacement=True,
                        insert_line_breaks=True,
                        convert_to_pem=True,
                        replace_header_footer=True,
                        encoded=True,
                    ),
                ),
            ]
        )

        modification = private_key_conditions_options_mapping.get_private_key_modification_option(
            is_unencrypted=is_unencrypted,
            is_encrypted=is_encrypted,
            has_line_breaks=has_line_breaks,
            has_private_key_passphrase=has_private_key_passphrase,
            lacks_headers_footers=lacks_headers_footers,
            is_encoded=is_encoded,
        )

        if is_unencrypted and has_line_breaks and private_key_passphrase:
            raise ValueError("Combination of unencrypted private key with private key passphrase is not supported")
        elif modification:
            data["private_key"] = modify_private_keys(private_key=private_key, **modification.model_dump())
            return data
        else:
            raise ValueError("Invalid private key format.")

    @model_validator(mode="after")
    def validate_auth_methods(self) -> typing_extensions.Self:
        """
        Validates that exactly one authentication method is provided.

        - Ensures that one and only one of the following is specified: `password`, `private_key`, or `private_key_file`.
        - Raises a `ValueError` if none or more than one authentication method is provided.

        Returns:
            typing_extensions.Self: The validated instance of the model.

        Raises:
            ValueError: If none or more than one authentication method is provided.
        """
        auth_methods = [self.password, self.private_key, self.private_key_file]
        provided_auth_methods = [auth_method for auth_method in auth_methods if auth_method is not None]

        if len(provided_auth_methods) != 1:
            raise ValueError("Exactly one of 'password', 'private_key', or 'path_to_private_key' must be provided.")
        return self
