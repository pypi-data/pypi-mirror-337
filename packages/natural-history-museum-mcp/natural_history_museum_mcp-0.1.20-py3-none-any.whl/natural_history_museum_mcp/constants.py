from enum import Enum


class NhmTools(str, Enum):
    SPECIMEN_SEARCH = "specimen_search"
    INDEX_LOTS_SEARCH = "index_lots_search"

DEFAULT_LIMIT = 100
DEFAULT_OFFSET = 0
