import typing as t

import pytest

from jamldump import to_jaml


@pytest.mark.parametrize(
    "value,level,embed_in,out",
    [
        ([], 0, "", "---\n[]\n...\n"),
        ({}, 0, "", "---\n{}\n...\n"),
        ("test", 0, "", '---\n"test"\n...\n'),
        ("test", 0, "document", '"test"'),
        ({}, 1, "dict", " {}"),
        ([], 1, "list", " []"),
        ({}, 1, "list", " {}"),
        ([], 1, "dict", " []"),
        ([{}], 0, "", "---\n- {}\n...\n"),
        ([[[]]], 0, "document", "- - []"),
        (
            {"a": [], "b": "test", "c": [True, False]},
            2,
            "list",
            """ a: []
    b: "test"
    c:
      - true
      - false""",
        ),
        ({"b": 1, "a": 0}, 0, "document", "a: 0\nb: 1"),
        ({"b": 1, "a": 0}, 0, "", "---\na: 0\nb: 1\n...\n"),
        ('"', 0, "document", '"\\""'),
        ("\\", 0, "document", '"\\\\"'),
    ],
)
def test_to_jaml(value: t.Any, level: int, embed_in: str, out: str) -> None:
    assert to_jaml(value, level, embed_in) == out
