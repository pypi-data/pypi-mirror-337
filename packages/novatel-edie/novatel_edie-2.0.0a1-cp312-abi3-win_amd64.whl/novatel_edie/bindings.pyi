from collections.abc import Mapping, Sequence
import enum
import os
from typing import overload

from . import enums as enums, messages as messages


class ASCII_HEADER(enum.IntEnum):
    """ASCII Message header format sequence"""

    def __str__(self) -> object: ...

    MESSAGE_NAME = 0
    """ASCII log Name."""

    PORT = 1
    """Receiver logging port."""

    SEQUENCE = 2
    """Embedded log sequence number."""

    IDLE_TIME = 3
    """Receiver Idle time."""

    TIME_STATUS = 4
    """GPS reference time status."""

    WEEK = 5
    """GPS Week number."""

    SECONDS = 6
    """GPS week seconds."""

    RECEIVER_STATUS = 7
    """Receiver status."""

    MSG_DEF_CRC = 8
    """Reserved Field."""

    RECEIVER_SW_VERSION = 9
    """Receiver software version."""

class ArrayField(BaseField):
    """Struct containing elements of array fields in the UI DB"""

    def __init__(self) -> None: ...

    @property
    def array_length(self) -> int: ...

    @array_length.setter
    def array_length(self, arg: int, /) -> None: ...

    def __repr__(self) -> str: ...

class BaseDataType:
    """Struct containing basic elements of data type fields in the UI DB"""

    def __init__(self) -> None: ...

    @property
    def name(self) -> DATA_TYPE: ...

    @name.setter
    def name(self, arg: DATA_TYPE, /) -> None: ...

    @property
    def length(self) -> int: ...

    @length.setter
    def length(self, arg: int, /) -> None: ...

    @property
    def description(self) -> str: ...

    @description.setter
    def description(self, arg: str, /) -> None: ...

class BaseField:
    """Struct containing elements of basic fields in the UI DB"""

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, name: str, type: FIELD_TYPE, conversion: str, length: int, data_type: DATA_TYPE) -> None: ...

    @property
    def name(self) -> str: ...

    @name.setter
    def name(self, arg: str, /) -> None: ...

    @property
    def type(self) -> FIELD_TYPE: ...

    @type.setter
    def type(self, arg: FIELD_TYPE, /) -> None: ...

    @property
    def description(self) -> str: ...

    @description.setter
    def description(self, arg: str, /) -> None: ...

    @property
    def conversion(self) -> str: ...

    @conversion.setter
    def conversion(self, arg: str, /) -> None: ...

    @property
    def conversion_before_point(self) -> int: ...

    @conversion_before_point.setter
    def conversion_before_point(self, arg: int, /) -> None: ...

    @property
    def conversion_after_point(self) -> int: ...

    @conversion_after_point.setter
    def conversion_after_point(self, arg: int, /) -> None: ...

    @property
    def data_type(self) -> SimpleDataType: ...

    @data_type.setter
    def data_type(self, arg: SimpleDataType, /) -> None: ...

    def set_conversion(self, conversion: str) -> None: ...

    def __repr__(self) -> str: ...

class BufferEmptyException(NovatelEdieException):
    pass

class BufferFullException(NovatelEdieException):
    pass

class Commander:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, message_db: MessageDatabase) -> None: ...

    def load_db(self, message_db: "novatel::edie::MessageDatabase") -> None: ...

    @property
    def logger(self) -> _SpdlogLogger: ...

    def encode(self, abbrev_ascii_command: bytes, encode_format: ENCODE_FORMAT) -> bytes: ...

class ConversionIterator:
    def __iter__(self) -> ConversionIterator: ...

    def __next__(self) -> object: ...

class DATA_TYPE(enum.IntEnum):
    """Data type name string represented as an enum"""

    def __str__(self) -> object: ...

    BOOL = 0

    CHAR = 1

    UCHAR = 2

    SHORT = 3

    USHORT = 4

    INT = 5

    UINT = 6

    LONG = 7

    ULONG = 8

    LONGLONG = 9

    ULONGLONG = 10

    FLOAT = 11

    DOUBLE = 12

    HEXBYTE = 13

    SATELLITEID = 14

    UNKNOWN = 15

class Decoder:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, message_db: MessageDatabase) -> None: ...

    @property
    def header_logger(self) -> _SpdlogLogger: ...

    @property
    def message_logger(self) -> _SpdlogLogger: ...

    def decode_header(self, raw_header: bytes, metadata: MetaData | None = None) -> Header: ...

    @overload
    def decode_message(self, raw_body: bytes, decoded_header: Header, metadata: MetaData) -> object: ...

    @overload
    def decode_message(self, raw_body: bytes, decoded_header: Header) -> object: ...

    def decode(self, message: bytes) -> object: ...

class DecoderException(Exception):
    pass

class DecompressionFailureException(NovatelEdieException):
    pass

class ENCODE_FORMAT(enum.IntEnum):
    def __str__(self) -> object: ...

    FLATTENED_BINARY = 0
    """
    NovAtel EDIE "Flattened" binary format.  All strings/arrays are padded to maximum length to allow programmatic access.
    """

    ASCII = 1
    """
    NovAtel ASCII. If the log was decoded from a SHORT/compressed format, it will be encoded to the respective SHORT/compressed format.
    """

    ABBREV_ASCII = 2
    """NovAtel Abbreviated ASCII."""

    BINARY = 3
    """
    NovAtel Binary. If the log was decoded from a SHORT/compressed format, it will be encoded to the respective SHORT/compressed format.
    """

    JSON = 4
    """A JSON object.  See HTML documentation for information on fields."""

    UNSPECIFIED = 5
    """No encode format was specified."""

class EnumDataType:
    """Enum Data Type representing contents of UI DB"""

    def __init__(self) -> None: ...

    @property
    def value(self) -> int: ...

    @value.setter
    def value(self, arg: int, /) -> None: ...

    @property
    def name(self) -> str: ...

    @name.setter
    def name(self, arg: str, /) -> None: ...

    @property
    def description(self) -> str: ...

    @description.setter
    def description(self, arg: str, /) -> None: ...

    def __repr__(self) -> str: ...

class EnumDefinition:
    """Enum Definition representing contents of UI DB"""

    def __init__(self) -> None: ...

    @property
    def id(self) -> str: ...

    @id.setter
    def id(self, arg: str, /) -> None: ...

    @property
    def name(self) -> str: ...

    @name.setter
    def name(self, arg: str, /) -> None: ...

    @property
    def enumerators(self) -> list[EnumDataType]: ...

    @enumerators.setter
    def enumerators(self, arg: Sequence[EnumDataType], /) -> None: ...

    def __repr__(self) -> str: ...

class EnumField(BaseField):
    """Struct containing elements of enum fields in the UI DB"""

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, name: str, enumerators: Sequence[EnumDataType]) -> None: ...

    @property
    def enum_id(self) -> str: ...

    @enum_id.setter
    def enum_id(self, arg: str, /) -> None: ...

    @property
    def enum_def(self) -> EnumDefinition: ...

    @enum_def.setter
    def enum_def(self, arg: EnumDefinition, /) -> None: ...

    @property
    def length(self) -> int: ...

    @length.setter
    def length(self, arg: int, /) -> None: ...

    def __repr__(self) -> str: ...

class FIELD_TYPE(enum.IntEnum):
    """Field type string represented as an enum."""

    def __str__(self) -> object: ...

    SIMPLE = 0

    ENUM = 1

    BITFIELD = 2

    FIXED_LENGTH_ARRAY = 3

    VARIABLE_LENGTH_ARRAY = 4

    STRING = 5

    FIELD_ARRAY = 6

    RESPONSE_ID = 7

    RESPONSE_STR = 8

    RXCONFIG_HEADER = 9

    RXCONFIG_BODY = 10

    UNKNOWN = 11

class FailureException(NovatelEdieException):
    pass

class Field:
    def to_dict(self) -> dict:
        """Convert the message and its sub-messages into a dict"""

    def __getattr__(self, field_name: str) -> object: ...

    def __repr__(self) -> str: ...

    def __dir__(self) -> list: ...

class FieldArrayField(BaseField):
    """Struct containing elements of field array fields in the UI DB"""

    def __init__(self) -> None: ...

    @property
    def array_length(self) -> int: ...

    @array_length.setter
    def array_length(self, arg: int, /) -> None: ...

    @property
    def field_size(self) -> int: ...

    @field_size.setter
    def field_size(self, arg: int, /) -> None: ...

    @property
    def fields(self) -> list[BaseField]: ...

    @fields.setter
    def fields(self, arg: Sequence[BaseField], /) -> None: ...

    def __repr__(self) -> str: ...

class FileConversionIterator:
    def __iter__(self) -> FileConversionIterator: ...

    def __next__(self) -> object: ...

class FileParser:
    @overload
    def __init__(self, file_path: str | os.PathLike) -> None: ...

    @overload
    def __init__(self, file_path: str | os.PathLike, message_db: MessageDatabase) -> None: ...

    @property
    def logger(self) -> _SpdlogLogger: ...

    def enable_framer_decoder_logging(self, level: LogLevel = LogLevel.DEBUG, filename: str = 'edie.log') -> None: ...

    @property
    def ignore_abbreviated_ascii_responses(self) -> bool: ...

    @ignore_abbreviated_ascii_responses.setter
    def ignore_abbreviated_ascii_responses(self, arg: bool, /) -> None: ...

    @property
    def decompress_range_cmp(self) -> bool: ...

    @decompress_range_cmp.setter
    def decompress_range_cmp(self, arg: bool, /) -> None: ...

    @property
    def return_unknown_bytes(self) -> bool: ...

    @return_unknown_bytes.setter
    def return_unknown_bytes(self, arg: bool, /) -> None: ...

    @property
    def filter(self) -> Filter: ...

    @filter.setter
    def filter(self, arg: Filter, /) -> None: ...

    def read() ->  Message | UnknownMessage | UnknownBytes:
        """
        Attempts to read a message from data in the FileParser's buffer.

        Returns:
            A decoded `Message`,
            an `UnknownMessage` whose header was identified but whose payload
            could not be decoded due to no available message definition,
            or a series of `UnknownBytes` determined to be undecodable.

        Raises:
            BufferEmptyException: There is insufficient data in the FileParser's
            buffer to decode a message.
        """

    def __iter__(self) -> FileParser: ...

    def __next__() -> Message | UnknownMessage | UnknownBytes:
        """
        Attempts to read the next message from data in the FileParser's buffer.

        Returns:
            A decoded `Message`,
            an `UnknownMessage` whose header was identified but whose payload
            could not be decoded due to no available message definition,
            or a series of `UnknownBytes` determined to be undecodable.

        Raises:
            StopIteration: There is insufficient data in the FileParser's
            buffer to decode a message.
        """

    def convert(self, fmt: ENCODE_FORMAT) -> object: ...

    def iter_convert(self, arg: ENCODE_FORMAT, /) -> FileConversionIterator: ...

    def reset(self) -> bool: ...

    def flush(self, return_flushed_bytes: bool = False) -> object: ...

    @property
    def internal_buffer(self) -> bytes: ...

class Filter:
    def __init__(self) -> None: ...

    @property
    def logger(self) -> _SpdlogLogger: ...

    def set_lower_time_bound(self, week: int, seconds: float) -> None: ...

    def set_upper_time_bound(self, week: int, seconds: float) -> None: ...

    def invert_time_filter(self, invert: bool) -> None: ...

    def set_include_decimation(self, period_sec: float) -> None: ...

    def invert_decimation_filter(self, invert: bool) -> None: ...

    @overload
    def include_time_status(self, time_status: TIME_STATUS) -> None: ...

    @overload
    def include_time_status(self, time_statuses: Sequence[TIME_STATUS]) -> None: ...

    def invert_time_status_filter(self, invert: bool) -> None: ...

    @overload
    def include_message_id(self, id: int, format: HEADER_FORMAT = HEADER_FORMAT.ALL, source: MEASUREMENT_SOURCE = MEASUREMENT_SOURCE.PRIMARY) -> None: ...

    @overload
    def include_message_id(self, ids: Sequence[tuple[int, HEADER_FORMAT, MEASUREMENT_SOURCE]]) -> None: ...

    def invert_message_id_filter(self, invert: bool) -> None: ...

    @overload
    def include_message_name(self, name: str, format: HEADER_FORMAT = HEADER_FORMAT.ALL, source: MEASUREMENT_SOURCE = MEASUREMENT_SOURCE.PRIMARY) -> None: ...

    @overload
    def include_message_name(self, names: Sequence[tuple[str, HEADER_FORMAT, MEASUREMENT_SOURCE]]) -> None: ...

    def invert_message_name_filter(self, invert: bool) -> None: ...

    def include_nmea_messages(self, include: bool) -> None: ...

    def clear_filters(self) -> None: ...

    def do_filtering(self, metadata: MetaData) -> bool: ...

class Framer:
    def __init__(self) -> None: ...

    @property
    def logger(self) -> _SpdlogLogger: ...

    def set_frame_json(self, frame_json: bool) -> None: ...

    def set_payload_only(self, payload_only: bool) -> None: ...

    def set_report_unknown_bytes(self, report_unknown_bytes: bool) -> None: ...

    @property
    def bytes_available_in_buffer(self) -> int: ...

    def get_frame(self, buffer_size: int = 32768) -> tuple: ...

    def __iter__(self) -> "novatel::edie::oem::Framer": ...

    def __next__(self) -> tuple: ...

    def write(self, arg: bytes, /) -> int: ...

    def flush(self) -> bytes: ...

class GpsTime:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, week: int, milliseconds: float, time_status: TIME_STATUS = TIME_STATUS.UNKNOWN) -> None: ...

    @property
    def week(self) -> int: ...

    @week.setter
    def week(self, arg: int, /) -> None: ...

    @property
    def milliseconds(self) -> float: ...

    @milliseconds.setter
    def milliseconds(self, arg: float, /) -> None: ...

    @property
    def status(self) -> TIME_STATUS: ...

    @status.setter
    def status(self, arg: TIME_STATUS, /) -> None: ...

class HEADER_FORMAT(enum.IntEnum):
    def __str__(self) -> object: ...

    UNKNOWN = 1

    BINARY = 2

    SHORT_BINARY = 3

    PROPRIETARY_BINARY = 4

    ASCII = 5

    SHORT_ASCII = 6

    ABB_ASCII = 7

    NMEA = 8

    JSON = 9

    SHORT_ABB_ASCII = 10

    ALL = 11

class Header:
    @property
    def message_id(self) -> int: ...

    @property
    def message_type(self) -> MessageType: ...

    @property
    def port_address(self) -> int: ...

    @property
    def length(self) -> int: ...

    @property
    def sequence(self) -> int: ...

    @property
    def idle_time(self) -> int: ...

    @property
    def time_status(self) -> int: ...

    @property
    def week(self) -> int: ...

    @property
    def milliseconds(self) -> float: ...

    @property
    def receiver_status(self) -> int: ...

    @property
    def message_definition_crc(self) -> int: ...

    @property
    def receiver_sw_version(self) -> int: ...

    def to_dict(self) -> dict: ...

    def __repr__(self) -> str: ...

class IncompleteException(NovatelEdieException):
    pass

class IncompleteMoreDataException(NovatelEdieException):
    pass

class JsonDbReaderException(NovatelEdieException):
    pass

class LogLevel(enum.Enum):
    def __str__(self) -> object: ...

    TRACE = 0

    DEBUG = 1

    INFO = 2

    WARN = 3

    ERR = 4

    CRITICAL = 5

    OFF = 6

class LogPatternTimeType(enum.Enum):
    LOCAL = 0

    UTC = 1

class Logging:
    def __init__(self) -> None: ...

    @staticmethod
    def get(logger_name: str) -> _SpdlogLogger:
        """Returns spdlog::get(logger_name)."""

    @staticmethod
    def shutdown() -> None:
        """Stop any running threads started by spdlog and clean registry loggers"""

    @staticmethod
    def set_logging_level(level: LogLevel) -> None:
        """Change the global spdlog logging level"""

    @staticmethod
    def register_logger(name: str) -> _SpdlogLogger:
        """Register a logger with the root logger's sinks."""

    @staticmethod
    def add_console_logging(logger: _SpdlogLogger, level: LogLevel = LogLevel.DEBUG) -> None:
        """Add console output to the logger"""

    @staticmethod
    def add_rotating_file_logger(logger: _SpdlogLogger, level: LogLevel = LogLevel.DEBUG, file_name: str = 'edie.log', file_size: int = 5242880, max_files: int = 2, rotate_on_open: bool = True) -> None:
        """Add rotating file output to the logger"""

MAX_ABB_ASCII_RESPONSE_LENGTH: int = 32768

MAX_ASCII_MESSAGE_LENGTH: int = 32768

MAX_BINARY_MESSAGE_LENGTH: int = 32768

MAX_NMEA_MESSAGE_LENGTH: int = 256

MAX_SHORT_ASCII_MESSAGE_LENGTH: int = 32768

MAX_SHORT_BINARY_MESSAGE_LENGTH: int = 271

class MEASUREMENT_SOURCE(enum.IntEnum):
    def __str__(self) -> object: ...

    PRIMARY = 0

    SECONDARY = 1

    MAX = 2

class MESSAGE_FORMAT(enum.IntEnum):
    def __str__(self) -> object: ...

    BINARY = 0

    ASCII = 1

    ABBREV = 2

    RSRVD = 3

class MESSAGE_ID_MASK(enum.IntEnum):
    def __str__(self) -> object: ...

    LOGID = 65535

    MEASSRC = 2031616

    MSGFORMAT = 6291456

    RESPONSE = 8388608

MESSAGE_SIZE_MAX: int = 32768

class MESSAGE_TYPE_MASK(enum.IntEnum):
    def __str__(self) -> object: ...

    MEASSRC = 31

    MSGFORMAT = 96

    RESPONSE = 128

class MalformedInputException(NovatelEdieException):
    pass

class Message(Field):
    def encode(self, arg: ENCODE_FORMAT, /) -> MessageData: ...

    def to_ascii(self) -> MessageData: ...

    def to_binary(self) -> MessageData: ...

    def to_flattended_binary(self) -> MessageData: ...

    def to_json(self) -> MessageData: ...

    def to_dict(self, include_header: bool = True) -> dict:
        """Convert the message its sub-fields into a dict"""

    @property
    def header(self) -> Header: ...

    @property
    def name(self) -> str: ...

class MessageData:
    def __repr__(self) -> str: ...

    @property
    def message(self) -> bytes: ...

    @property
    def header(self) -> object: ...

    @property
    def body(self) -> object: ...

class MessageDatabase:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, file_path: str | os.PathLike) -> None: ...

    @staticmethod
    def from_string(json_data: str) -> MessageDatabase: ...

    def merge(self, other_db: "novatel::edie::MessageDatabase") -> None: ...

    def append_messages(self, messages: Sequence[MessageDefinition]) -> None: ...

    def append_enumerations(self, enums: Sequence[EnumDefinition]) -> None: ...

    def remove_message(self, msg_id: int) -> None: ...

    def remove_enumeration(self, enumeration: str) -> None: ...

    @overload
    def get_msg_def(self, msg_name: str) -> MessageDefinition: ...

    @overload
    def get_msg_def(self, msg_id: int) -> MessageDefinition: ...

    @overload
    def get_enum_def(self, enum_id: str) -> EnumDefinition: ...

    @overload
    def get_enum_def(self, enum_name: str) -> EnumDefinition: ...

    def get_msg_type(self, name: str) -> object: ...

    def get_enum_type_by_name(self, name: str) -> object: ...

    def get_enum_type_by_id(self, id: str) -> object: ...

class MessageDefinition:
    """Struct containing elements of message definitions in the UI DB"""

    def __init__(self) -> None: ...

    @property
    def id(self) -> str: ...

    @id.setter
    def id(self, arg: str, /) -> None: ...

    @property
    def log_id(self) -> int: ...

    @log_id.setter
    def log_id(self, arg: int, /) -> None: ...

    @property
    def name(self) -> str: ...

    @name.setter
    def name(self, arg: str, /) -> None: ...

    @property
    def description(self) -> str: ...

    @description.setter
    def description(self, arg: str, /) -> None: ...

    @property
    def fields(self) -> dict: ...

    @property
    def latest_message_crc(self) -> int: ...

    @latest_message_crc.setter
    def latest_message_crc(self, arg: int, /) -> None: ...

    def __repr__(self) -> str: ...

class MessageType:
    def __repr__(self) -> str: ...

    @property
    def is_response(self) -> bool: ...

    @property
    def format(self) -> MESSAGE_FORMAT: ...

    @property
    def source(self) -> MEASUREMENT_SOURCE: ...

class MetaData:
    def __init__(self) -> None: ...

    @property
    def format(self) -> HEADER_FORMAT: ...

    @format.setter
    def format(self, arg: HEADER_FORMAT, /) -> None: ...

    @property
    def measurement_source(self) -> MEASUREMENT_SOURCE: ...

    @measurement_source.setter
    def measurement_source(self, arg: MEASUREMENT_SOURCE, /) -> None: ...

    @property
    def time_status(self) -> TIME_STATUS: ...

    @time_status.setter
    def time_status(self, arg: TIME_STATUS, /) -> None: ...

    @property
    def response(self) -> bool: ...

    @response.setter
    def response(self, arg: bool, /) -> None: ...

    @property
    def week(self) -> int: ...

    @week.setter
    def week(self, arg: int, /) -> None: ...

    @property
    def milliseconds(self) -> float: ...

    @milliseconds.setter
    def milliseconds(self, arg: float, /) -> None: ...

    @property
    def binary_msg_length(self) -> int:
        """
        Message length according to the binary header. If ASCII, this field is not used.
        """

    @binary_msg_length.setter
    def binary_msg_length(self, arg: int, /) -> None: ...

    @property
    def length(self) -> int:
        """Length of the entire log, including the header and CRC."""

    @length.setter
    def length(self, arg: int, /) -> None: ...

    @property
    def header_length(self) -> int:
        """The length of the message header. Used for NovAtel logs."""

    @header_length.setter
    def header_length(self, arg: int, /) -> None: ...

    @property
    def message_id(self) -> int: ...

    @message_id.setter
    def message_id(self, arg: int, /) -> None: ...

    @property
    def message_crc(self) -> int: ...

    @message_crc.setter
    def message_crc(self, arg: int, /) -> None: ...

    @property
    def message_name(self) -> str: ...

    @message_name.setter
    def message_name(self, arg: str, /) -> None: ...

    @property
    def message_description(self) -> object: ...

    @property
    def message_fields(self) -> object: ...

    def __repr__(self) -> str: ...

NMEA_CRC_LENGTH: int = 2

NMEA_SYNC: str = '$'

NMEA_SYNC_LENGTH: int = 1

class NoDatabaseException(NovatelEdieException):
    pass

class NoDefinitionEmbeddedException(NovatelEdieException):
    pass

class NoDefinitionException(NovatelEdieException):
    pass

class NovatelEdieException(Exception):
    pass

class NullProvidedException(NovatelEdieException):
    pass

OEM4_ABBREV_ASCII_INDENTATION_LENGTH: int = 5

OEM4_ABBREV_ASCII_SEPARATOR: str = ' '

OEM4_ABBREV_ASCII_SYNC: str = '<'

OEM4_ASCII_CRC_DELIMITER: str = '*'

OEM4_ASCII_CRC_LENGTH: int = 8

OEM4_ASCII_FIELD_SEPARATOR: str = ','

OEM4_ASCII_HEADER_TERMINATOR: str = ';'

OEM4_ASCII_MESSAGE_NAME_MAX: int = 40

OEM4_ASCII_SYNC: str = '#'

OEM4_ASCII_SYNC_LENGTH: int = 1

OEM4_BINARY_CRC_LENGTH: int = 4

OEM4_BINARY_HEADER_LENGTH: int = 28

OEM4_BINARY_SYNC1: int = 170

OEM4_BINARY_SYNC2: int = 68

OEM4_BINARY_SYNC3: int = 18

OEM4_BINARY_SYNC_LENGTH: int = 3

OEM4_ERROR_PREFIX_LENGTH: int = 6

OEM4_PROPRIETARY_BINARY_SYNC2: int = 69

OEM4_SHORT_ASCII_SYNC: str = '%'

OEM4_SHORT_ASCII_SYNC_LENGTH: int = 1

OEM4_SHORT_BINARY_HEADER_LENGTH: int = 12

OEM4_SHORT_BINARY_SYNC3: int = 19

OEM4_SHORT_BINARY_SYNC_LENGTH: int = 3

class Oem4BinaryHeader:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: bytes, /) -> None: ...

    @property
    def sync1(self) -> int:
        """First sync byte of Header."""

    @sync1.setter
    def sync1(self, arg: int, /) -> None: ...

    @property
    def sync2(self) -> int:
        """Second sync byte of Header."""

    @sync2.setter
    def sync2(self, arg: int, /) -> None: ...

    @property
    def sync3(self) -> int:
        """Third sync byte of Header."""

    @sync3.setter
    def sync3(self, arg: int, /) -> None: ...

    @property
    def header_length(self) -> int:
        """Total Binary header length."""

    @header_length.setter
    def header_length(self, arg: int, /) -> None: ...

    @property
    def msg_number(self) -> int:
        """Binary log Message Number/ID."""

    @msg_number.setter
    def msg_number(self, arg: int, /) -> None: ...

    @property
    def msg_type(self) -> int:
        """Binary log Message type response or data?."""

    @msg_type.setter
    def msg_type(self, arg: int, /) -> None: ...

    @property
    def port(self) -> int:
        """Receiver Port of logging."""

    @port.setter
    def port(self, arg: int, /) -> None: ...

    @property
    def length(self) -> int:
        """Total length of binary log."""

    @length.setter
    def length(self, arg: int, /) -> None: ...

    @property
    def sequence_number(self) -> int:
        """Sequence number of Embedded message inside."""

    @sequence_number.setter
    def sequence_number(self, arg: int, /) -> None: ...

    @property
    def idle_time(self) -> int:
        """Receiver Idle time."""

    @idle_time.setter
    def idle_time(self, arg: int, /) -> None: ...

    @property
    def time_status(self) -> int:
        """GPS reference time status."""

    @time_status.setter
    def time_status(self, arg: int, /) -> None: ...

    @property
    def week_no(self) -> int:
        """GPS Week number."""

    @week_no.setter
    def week_no(self, arg: int, /) -> None: ...

    @property
    def week_msec(self) -> int:
        """GPS week seconds."""

    @week_msec.setter
    def week_msec(self, arg: int, /) -> None: ...

    @property
    def status(self) -> int:
        """Status of the log."""

    @status.setter
    def status(self, arg: int, /) -> None: ...

    @property
    def msg_def_crc(self) -> int:
        """Message def CRC of binary log."""

    @msg_def_crc.setter
    def msg_def_crc(self, arg: int, /) -> None: ...

    @property
    def receiver_sw_version(self) -> int:
        """Receiver Software version."""

    @receiver_sw_version.setter
    def receiver_sw_version(self, arg: int, /) -> None: ...

    def __bytes__(self) -> bytes: ...

    def __repr__(self) -> str: ...

class Oem4BinaryShortHeader:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: bytes, /) -> None: ...

    @property
    def sync1(self) -> int:
        """First sync byte of Header."""

    @sync1.setter
    def sync1(self, arg: int, /) -> None: ...

    @property
    def sync2(self) -> int:
        """Second sync byte of Header."""

    @sync2.setter
    def sync2(self, arg: int, /) -> None: ...

    @property
    def sync3(self) -> int:
        """Third sync byte of Header."""

    @sync3.setter
    def sync3(self, arg: int, /) -> None: ...

    @property
    def length(self) -> int:
        """Message body length."""

    @length.setter
    def length(self, arg: int, /) -> None: ...

    @property
    def message_id(self) -> int:
        """Message ID of the log."""

    @message_id.setter
    def message_id(self, arg: int, /) -> None: ...

    @property
    def week_no(self) -> int:
        """GPS Week number."""

    @week_no.setter
    def week_no(self, arg: int, /) -> None: ...

    @property
    def week_msec(self) -> int:
        """GPS Week seconds."""

    @week_msec.setter
    def week_msec(self, arg: int, /) -> None: ...

    def __bytes__(self) -> bytes: ...

    def __repr__(self) -> str: ...

class Parser:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, message_db: MessageDatabase) -> None: ...

    @property
    def logger(self) -> _SpdlogLogger: ...

    def enable_framer_decoder_logging(self, level: LogLevel = LogLevel.DEBUG, filename: str = 'edie.log') -> None: ...

    @property
    def ignore_abbreviated_ascii_responses(self) -> bool: ...

    @ignore_abbreviated_ascii_responses.setter
    def ignore_abbreviated_ascii_responses(self, arg: bool, /) -> None: ...

    @property
    def decompress_range_cmp(self) -> bool: ...

    @decompress_range_cmp.setter
    def decompress_range_cmp(self, arg: bool, /) -> None: ...

    @property
    def return_unknown_bytes(self) -> bool: ...

    @return_unknown_bytes.setter
    def return_unknown_bytes(self, arg: bool, /) -> None: ...

    @property
    def filter(self) -> Filter: ...

    @filter.setter
    def filter(self, arg: Filter, /) -> None: ...

    def write(self, arg: bytes, /) -> int: ...

    def read(decode_incomplete_abbreviated=False) -> Message | UnknownMessage | UnknownBytes:
        """
        Attempts to read a message from data in the Parser's buffer.

        Args:
            decode_incomplete_abbreviated: If True, the Parser will try to
                interpret a possibly incomplete abbreviated ASCII message as if
                it were complete. This is necessary when there is no data
                following the message to indicate that its end.

        Returns:
            A decoded `Message`,
            an `UnknownMessage` whose header was identified but whose payload
            could not be decoded due to no available message definition,
            or a series of `UnknownBytes` determined to be undecodable.

        Raises:
            BufferEmptyException: There is insufficient data in the Parser's
            buffer to decode a message.
        """

    def __iter__(self) -> Parser: ...

    def __next__() -> Message | UnknownMessage | UnknownBytes:
        """
        Attempts to read the next message from data in the Parser's buffer.

        Returns:
            A decoded `Message`,
            an `UnknownMessage` whose header was identified but whose payload
            could not be decoded due to no available message definition,
            or a series of `UnknownBytes` determined to be undecodable.

        Raises:
            StopIteration: There is insufficient data in the Parser's
            buffer to decode a message.
        """

    def convert(self, fmt: ENCODE_FORMAT, decode_incomplete_abbreviated: bool = False) -> object: ...

    def iter_convert(self, fmt: ENCODE_FORMAT) -> ConversionIterator: ...

    def flush(self, return_flushed_bytes: bool = False) -> object: ...

    @property
    def internal_buffer(self) -> bytes: ...

class RangeDecompressor:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, message_db: MessageDatabase) -> None: ...

    @property
    def logger(self) -> _SpdlogLogger: ...

    def reset(self) -> None: ...

    def decompress(self, data: bytes, metadata: MetaData, encode_format: ENCODE_FORMAT = ENCODE_FORMAT.UNSPECIFIED) -> object: ...

class RxConfigHandler:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, message_db: MessageDatabase) -> None: ...

    def load_db(self, message_db: "novatel::edie::MessageDatabase") -> None: ...

    @property
    def logger(self) -> _SpdlogLogger: ...

    def write(self, arg: bytes, /) -> int: ...

    def convert(self, encode_format: ENCODE_FORMAT) -> tuple: ...

    def flush(self, return_flushed_bytes: bool = False) -> object: ...

class STATUS(enum.IntEnum):
    def __str__(self) -> object: ...

    SUCCESS = 0
    """Successfully found a frame in the framer buffer."""

    FAILURE = 1
    """An unexpected failure occurred."""

    UNKNOWN = 2
    """Could not identify bytes as a protocol."""

    INCOMPLETE = 3
    """
    It is possible that a valid frame exists in the frame buffer, but more information is needed.
    """

    INCOMPLETE_MORE_DATA = 4
    """The current frame buffer is incomplete but more data is expected."""

    NULL_PROVIDED = 5
    """A null pointer was provided."""

    NO_DATABASE = 6
    """No database has been provided to the component."""

    NO_DEFINITION = 7
    """No definition could be found in the database for the provided message."""

    NO_DEFINITION_EMBEDDED = 8
    """
    No definition could be found in the database for the embedded message in the RXCONFIG log.
    """

    BUFFER_FULL = 9
    """
    The provided destination buffer is not big enough to contain the frame.
    """

    BUFFER_EMPTY = 10
    """The internal circular buffer does not contain any unread bytes"""

    STREAM_EMPTY = 11
    """The input stream is empty."""

    UNSUPPORTED = 12
    """An attempted operation is unsupported by this component."""

    MALFORMED_INPUT = 13
    """The input is recognizable, but has unexpected formatting."""

    DECOMPRESSION_FAILURE = 14
    """The RANGECMPx log could not be decompressed."""

    def raise_on_error(self, message: str = '') -> None: ...

class SatelliteId:
    def __init__(self) -> None: ...

    @property
    def prn_or_slot(self) -> int: ...

    @prn_or_slot.setter
    def prn_or_slot(self, arg: int, /) -> None: ...

    @property
    def frequency_channel(self) -> int: ...

    @frequency_channel.setter
    def frequency_channel(self, arg: int, /) -> None: ...

    def __repr__(self) -> str: ...

class SimpleDataType(BaseDataType):
    """Struct containing elements of simple data type fields in the UI DB"""

    def __init__(self) -> None: ...

    @property
    def enums(self) -> dict[int, EnumDataType]: ...

    @enums.setter
    def enums(self, arg: Mapping[int, EnumDataType], /) -> None: ...

class StreamEmptyException(NovatelEdieException):
    pass

class TIME_STATUS(enum.IntEnum):
    def __str__(self) -> object: ...

    UNKNOWN = 20
    """Time validity is unknown."""

    APPROXIMATE = 60
    """Time is set approximately."""

    COARSEADJUSTING = 80
    """Time is approaching coarse precision."""

    COARSE = 100
    """This time is valid to coarse precision."""

    COARSESTEERING = 120
    """Time is coarse set and is being steered."""

    FREEWHEELING = 130
    """Position is lost and the range bias cannot be calculated."""

    FINEADJUSTING = 140
    """Time is adjusting to fine precision."""

    FINE = 160
    """Time has fine precision."""

    FINEBACKUPSTEERING = 170
    """Time is fine set and is being steered by the backup system."""

    FINESTEERING = 180
    """Time is fine set and is being steered."""

    SATTIME = 200
    """
    Time from satellite. Only used in logs containing satellite data such as ephemeris and almanac.
    """

    EXTERN = 220
    """Time source is external to the Receiver."""

    EXACT = 240
    """Time is exact."""

class UnknownBytes:
    def __repr__(self) -> str: ...

    @property
    def data(self) -> bytes: ...

class UnknownException(NovatelEdieException):
    pass

class UnknownMessage:
    def __repr__(self) -> str: ...

    @property
    def header(self) -> Header: ...

    @property
    def payload(self) -> bytes: ...

    def to_dict(self) -> dict:
        """Convert to a dict"""

class UnsupportedException(NovatelEdieException):
    pass

build_timestamp: str = '0000-00-00T00:00:00'

def get_default_database() -> MessageDatabase:
    """Get the default JSON database singleton"""

git_branch: str = ''

git_is_dirty: bool = False

git_sha: str = '0000000000000000'

pretty_version: str = 'Version: 3.5.0\nBranch: \nSHA: 0000000000000000'

str_to_DATA_TYPE: dict = ...

str_to_FIELD_TYPE: dict = ...

def string_to_encode_format(str: str) -> ENCODE_FORMAT: ...

def throw_exception_from_status(status: STATUS) -> None: ...

version: str = '3.5.0'
