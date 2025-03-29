from enum import Enum

class PolicyAssignmentType(Enum):
    """
    Enum for valid policy assignment types
    """

    TABLECOLUMNS = "TABLECOLUMNS"
    VIEWCOLUMNS = "VIEWCOLUMNS"
    VIEWS = "VIEWS"
    TABLES = "TABLES"
    TAGS = "TAGS"

