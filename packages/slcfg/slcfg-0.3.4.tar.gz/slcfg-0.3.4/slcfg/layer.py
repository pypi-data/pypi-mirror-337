import abc
import base64
import dataclasses
import io
import json
import os
import tomllib
import typing

from slcfg import item, util

type _AbstractTransformer[T, S] = typing.Callable[[T], S]
type Layer = Source[item.Items]


@dataclasses.dataclass
class Source[T](abc.ABC):
    getter: typing.Callable[[], T]

    def __or__[S](self, t: _AbstractTransformer[T, S]):
        return Source(getter=lambda: t(self.getter()))


@dataclasses.dataclass
class Transformer[T, S]:
    handler: _AbstractTransformer[T, S]

    def __call__(self, t: T):
        return self.handler(t)

    def __or__[U](self, other: _AbstractTransformer[S, U]):
        return Transformer[T, U](handler=lambda t: other(self.handler(t)))


### Sources


def source[T](v: T) -> Source[T]:
    return Source(getter=lambda: v)


def file_source(path: util.PathLike, *, default: bytes | None = None):
    def getter():
        try:
            return io.BytesIO(path.read_bytes())
        except FileNotFoundError:
            if default is not None:
                return io.BytesIO(default)
            raise

    return Source(getter=getter)


def env_source():
    return Source(getter=lambda: list(os.environ.items()))


def env_var_source(name: str, *, default: str | None = None):
    def getter():
        if (value := os.environ.get(name)) is not None:
            return value
        if default is not None:
            return default
        raise KeyError(name)

    return Source(getter=getter)


### Transformers


base64_transform = Transformer(base64.b64decode) | io.BytesIO
hex_transform = Transformer(bytes.fromhex) | io.BytesIO
utf8_transform = Transformer(str.encode) | io.BytesIO
json_transform = Transformer(json.load) | item.list_items
toml_transform = Transformer(tomllib.load) | item.list_items


def _case_transform(items: list[tuple[str, str]]):
    return [(k.lower(), v) for k, v in items]


def _prefix_transform(prefix: str):
    def transormer(items: list[tuple[str, str]]):
        return [(k.removeprefix(prefix), v) for k, v in items if k.startswith(prefix)]

    return transormer


def _delimiter_transform(delimiter: str):
    def transormer(items: list[tuple[str, str]]):
        return [(k.split(delimiter), v) for k, v in items]

    return transormer


def item_transform(items: list[tuple[list[str], str]]) -> item.Items:
    return [item.Item(k, v) for k, v in items]


### Shortcuts


def json_file_layer(path: util.PathLike, *, optional: bool = False):
    return file_source(path, default=b'{}' if optional else None) | json_transform


def toml_file_layer(path: util.PathLike, *, optional: bool = False):
    return file_source(path, default=b'' if optional else None) | toml_transform


def env_base64_json_layer(var_name: str, *, optional: bool = False):
    return (
        env_var_source(var_name, default=base64.b64encode(b'{}').decode() if optional else None)
        | base64_transform
        | json_transform
    )


def env_base64_toml_layer(var_name: str, *, optional: bool = False):
    return (
        env_var_source(var_name, default='' if optional else None)
        | base64_transform
        | toml_transform
    )


def env_layer(prefix: str, nested_delimiter: str, *, case_sensitive: bool = False):
    source = env_source()

    if not case_sensitive:
        prefix = prefix.lower()
        nested_delimiter = nested_delimiter.lower()
        source = source | _case_transform

    return (
        source | _prefix_transform(prefix) | _delimiter_transform(nested_delimiter) | item_transform
    )


def value_layer(value: item.ValueTree):
    return source(value) | item.list_items
