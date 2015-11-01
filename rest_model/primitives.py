"""Implement the building blocks of data types using Descriptor protocol."""


class Descriptor:
    """Store attribute name with associated value."""

    def __init__(self, name=None):
        """Initialize the descriptor."""
        self._name = name

    def __set__(self, instance, value):
        """Set the value."""
        instance.__dict__[self._name] = value


class Typed(Descriptor):
    """Add type checking to attributes."""

    _expected_type = type(None)

    def __set__(self, instance, value):
        """Validate type and set value."""
        if not isinstance(value, self._expected_type):
            raise TypeError("expected {}".format(self._expected_type))
        super().__set__(instance, value)


class Integer(Typed):
    """Add integer data building block."""

    _expected_type = int


class Float(Typed):
    """Add float data building block."""

    _expected_type = float


class String(Typed):
    """Add string data building block."""

    _expected_type = str


class List(Typed):
    """Add list data building block."""

    _expected_type = list


class Positive(Descriptor):
    """Add positive number building block."""

    def __set__(self, instance, value):
        """Check attribute value is a positive number."""
        if value < 0:
            raise TypeError("Expected value to be >= 0")
        super().__set__(instance, value)
