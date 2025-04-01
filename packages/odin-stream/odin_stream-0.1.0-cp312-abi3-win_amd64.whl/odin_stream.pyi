from collections.abc import Iterable
import enum


E_BADHASH: StreamingPacketStatus = StreamingPacketStatus.E_BADHASH

E_BADSIZE: StreamingPacketStatus = StreamingPacketStatus.E_BADSIZE

E_BADTYPE: StreamingPacketStatus = StreamingPacketStatus.E_BADTYPE

E_DUPLICATE: ParameterSetStatus = ParameterSetStatus.E_DUPLICATE

E_FULL: ParameterSetStatus = ParameterSetStatus.E_FULL

E_INTERNAL: StreamingPacketStatus = StreamingPacketStatus.E_INTERNAL

E_INVALID: StreamingPacketStatus = StreamingPacketStatus.E_INVALID

E_NODATA: StreamingPacketStatus = StreamingPacketStatus.E_NODATA

E_NOMEM: StreamingPacketStatus = StreamingPacketStatus.E_NOMEM

E_NOTFOUND: ParameterSetStatus = ParameterSetStatus.E_NOTFOUND

E_OVERFLOW: StreamingPacketStatus = StreamingPacketStatus.E_OVERFLOW

class FixedSizeParameter:
    """Wrapper for parameter descriptor (index/data)"""

    def __init__(self, index: int, data: bytes) -> None:
        """Create a parameter descriptor. Size is derived from data."""

    @property
    def index(self) -> int:
        """Parameter index (uint32)"""

    @index.setter
    def index(self, arg: int, /) -> None: ...

    @property
    def data(self) -> bytes:
        """Parameter data (bytes), updates size implicitly."""

    @data.setter
    def data(self, arg: bytes, /) -> None: ...

    @property
    def size(self) -> int:
        """Size of parameter data in bytes (derived from data)."""

    def __repr__(self) -> str: ...

class ParameterSet:
    """Manages a set of streaming parameters"""

    def __init__(self, max_parameters: int) -> None:
        """Create a new, empty parameter set with a maximum capacity."""

    def add(self, parameter: FixedSizeParameter) -> None:
        """Add a parameter descriptor (FixedSizeParameter) to the set."""

    def add_list(self, parameters: Iterable) -> None:
        """Add multiple parameter descriptors from a Python iterable."""

    def remove_by_index(self, index: int) -> None:
        """Remove a parameter from the set by its index."""

    def generate_identifier_packet(self) -> bytes:
        """Generate the identifier packet for this set as bytes."""

    def generate_data_packet(self, timestamp: int) -> bytes:
        """Generate the data packet for this set as bytes, including a timestamp."""

    @property
    def count(self) -> int:
        """Current number of parameters."""

    @property
    def max_count(self) -> int:
        """Maximum capacity."""

    @property
    def hash(self) -> int:
        """Current parameter index hash (CRC16)."""

    @property
    def indices(self) -> list[int]:
        """List of indices currently in the set."""

    def __len__(self) -> int: ...

    def __repr__(self) -> str: ...

    def parse_data_packet(self, data: bytes) -> list[bytes]:
        """
        Parses a data packet (bytes), verifies against the set definition,
        and returns a list of bytes objects containing the data for each parameter.
        """

    @staticmethod
    def parse_identifier_packet(data: bytes) -> ParameterSet:
        """
        Parse an identifier packet (bytes) and create a new ParameterSet instance.
        """

class ParameterSetStatus(enum.Enum):
    SUCCESS = 0

    E_NOMEM = -1

    E_FULL = -2

    E_DUPLICATE = -3

    E_NOTFOUND = -4

    E_INVALID = -5

    E_INTERNAL = -6

SUCCESS: StreamingPacketStatus = StreamingPacketStatus.SUCCESS

class StreamingPacketStatus(enum.Enum):
    SUCCESS = 0

    E_INVALID = -1

    E_BADSIZE = -2

    E_BADTYPE = -3

    E_BADHASH = -4

    E_NODATA = -5

    E_OVERFLOW = -6

    E_INTERNAL = -7

    E_NOMEM = -8
