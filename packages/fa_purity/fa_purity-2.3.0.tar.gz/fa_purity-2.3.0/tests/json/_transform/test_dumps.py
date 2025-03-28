from decimal import (
    Decimal,
)

from fa_purity._core.frozen import FrozenDict
from fa_purity._core.unsafe import Unsafe
from fa_purity.json import (
    JsonUnfolder,
    JsonValue,
)
from fa_purity.json._core.primitive import JsonPrimitive
from fa_purity.json._transform.value._factory._jval_factory import JsonValueFactory
from fa_purity.json._transform.value._transform import Unfolder


def test_dumps() -> None:
    test_data = (
        JsonValueFactory.from_any({"foo": {"nested": ["hi", 99]}, "foo2": Decimal("123.44")})
        .bind(Unfolder.to_json)
        .alt(Unsafe.raise_exception)
        .to_union()
    )
    assert JsonUnfolder.dumps(test_data).replace(
        " ",
        "",
    ) == '{"foo": {"nested": ["hi", 99]}, "foo2": 123.44}'.replace(" ", "")


def test_from_any() -> None:
    result = (
        JsonValueFactory.from_any({"foo": {"nested": ["hi", 99]}, "foo2": Decimal("123.44")})
        .bind(Unfolder.to_json)
        .alt(Unsafe.raise_exception)
        .to_union()
    )
    nested = FrozenDict(
        {
            "nested": JsonValue.from_list(
                (
                    JsonValue.from_primitive(JsonPrimitive.from_str("hi")),
                    JsonValue.from_primitive(JsonPrimitive.from_int(99)),
                ),
            ),
        },
    )
    expected = FrozenDict(
        {
            "foo": JsonValue.from_json(nested),
            "foo2": JsonValue.from_primitive(JsonPrimitive.from_decimal(Decimal("123.44"))),
        },
    )
    assert result == expected
