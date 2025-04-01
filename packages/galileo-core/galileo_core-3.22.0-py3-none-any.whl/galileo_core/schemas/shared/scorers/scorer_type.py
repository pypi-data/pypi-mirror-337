from enum import Enum
from typing import Literal


class CodeScorerLanguage(str, Enum):
    """Supported sandbox languages."""

    python = "python"
    typescript = "typescript"


class ScorerType(str, Enum):
    luna = "luna"
    plus = "plus"


PlusScorerType = Literal[ScorerType.plus]
LunaOrPlusScorerType = Literal[ScorerType.luna, ScorerType.plus]
