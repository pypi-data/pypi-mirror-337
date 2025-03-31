import typing


class PathLike(typing.Protocol):
    def read_bytes(self) -> bytes: ...


def is_dict_instance[K, V](
    d: object, key_type: type[K], value_type: type[V]
) -> typing.TypeGuard[dict[K, V]]:
    return isinstance(d, dict) and all(
        isinstance(k, key_type) and isinstance(v, value_type)
        for k, v in typing.cast('dict[object, object]', d).items()
    )
