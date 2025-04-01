from enum import Enum
from typing import Literal


class CodeScorerLanguage(str, Enum):
    """Supported sandbox languages."""

    python = "python"
    javascript = "javascript"

    @property
    def file_extension(self) -> str:
        """Get the file extension for this language."""
        extensions = {
            CodeScorerLanguage.python: ".py",
            CodeScorerLanguage.javascript: ".js",
        }
        return extensions.get(self, "")  # Default to nothing if language isn't recognized


class ScorerType(str, Enum):
    luna = "luna"
    plus = "plus"


PlusScorerType = Literal[ScorerType.plus]
LunaOrPlusScorerType = Literal[ScorerType.luna, ScorerType.plus]
