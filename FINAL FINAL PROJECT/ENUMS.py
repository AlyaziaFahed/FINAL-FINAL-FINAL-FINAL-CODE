from enum import Enum, auto


class ServiceType(Enum):
    CATERING = "Catering"
    CLEANING = "Cleaning"
    DECORATIONS = "Decorations"
    ENTERTAINMENT = "Entertainment"
    FURNITURE = "Furniture"


class EventType(Enum):
    WEDDING = auto()
    BIRTHDAY = auto()
    THEMED_PARTY = auto()
    GRADUATION = auto()
