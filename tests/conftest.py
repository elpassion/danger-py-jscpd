from typing import Any, Dict, Iterator, List
from unittest.mock import patch

import pytest
from danger_python.danger import Danger
from danger_python.models import DangerDSLJSONType


@pytest.fixture
def modified_files() -> List[str]:
    return []


@pytest.fixture
def created_files() -> List[str]:
    return []


@pytest.fixture
def deleted_files() -> List[str]:
    return []


@pytest.fixture
def danger_json(
    modified_files: List[str], created_files: List[str], deleted_files: List[str]
) -> Dict[str, Any]:
    return {
        "git": {
            "modified_files": modified_files,
            "created_files": created_files,
            "deleted_files": deleted_files,
        }
    }


@pytest.fixture
def danger(danger_json: Dict[str, Any]) -> Iterator[Danger]:
    with patch("danger_python.danger.load_dsl") as load_dsl:
        load_dsl.return_value = DangerDSLJSONType(**danger_json)
        Danger.dsl = None
        Danger.results = None
        yield Danger()

    Danger.dsl = None
    Danger.results = None
