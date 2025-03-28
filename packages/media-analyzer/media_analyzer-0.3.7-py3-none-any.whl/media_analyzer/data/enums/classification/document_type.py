from enum import StrEnum, auto


class DocumentType(StrEnum):
    """Document types enum."""

    BOOK_OR_MAGAZINE = auto()
    RECEIPT = auto()
    SCREENSHOT = auto()
    TICKET = auto()
    IDENTITY = auto()
    NOTES = auto()
    PAYMENT_METHOD = auto()
    MENU = auto()
    RECIPE = auto()
