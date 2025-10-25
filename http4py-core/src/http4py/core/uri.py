from __future__ import annotations

import re
from dataclasses import dataclass, replace
from urllib.parse import quote, unquote


def _url_encode(s: str) -> str:
    return quote(s, safe="")


def _url_decode(s: str) -> str:
    return unquote(s)


def _to_parameters(query: str) -> list[tuple[str, str | None]]:
    if not query:
        return []
    return [_to_parameter(param) for param in query.split("&")]


def _to_parameter(param: str) -> tuple[str, str | None]:
    parts = param.split("=", 1)
    key = _url_decode(parts[0])
    value = _url_decode(parts[1]) if len(parts) > 1 else None
    return (key, value)


def _to_url_form_encoded(params: list[tuple[str, str | None]]) -> str:
    def encode_param(key: str, value: str | None) -> str:
        encoded_key = _url_encode(key)
        if value is None:
            return encoded_key
        return f"{encoded_key}={_url_encode(value)}"

    return "&".join(encode_param(k, v) for k, v in params)


@dataclass
class Uri:
    scheme: str = ""
    userinfo: str = ""
    host: str = ""
    port: int | None = None
    path: str = ""
    query: str = ""
    fragment: str = ""

    @classmethod
    def of(cls, uri: str) -> Uri:
        match = cls._RFC3986.match(uri)
        if not match:
            raise ValueError(f"Invalid URI: {uri}")

        scheme, authority, path, query, fragment = match.groups()
        scheme = scheme or ""
        authority = authority or ""
        path = path or ""
        query = query or ""
        fragment = fragment or ""

        userinfo, host, port = cls._parse_authority(authority)

        return cls(scheme, userinfo, host, port, path, query, fragment)

    _RFC3986 = re.compile(r"^(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*)(?:\?([^#]*))?(?:#(.*))?")
    _AUTHORITY = re.compile(r"(?:([^@]+)@)?([^:]+)(?::(\d+))?")

    @classmethod
    def _parse_authority(cls, authority: str) -> tuple[str, str, int | None]:
        if not authority:
            return "", "", None

        match = cls._AUTHORITY.match(authority)
        if not match:
            raise ValueError(f"Invalid authority: {authority}")

        userinfo, host, port_str = match.groups()
        userinfo = userinfo or ""
        host = host or ""
        port = int(port_str) if port_str else None

        return userinfo, host, port

    @property
    def authority(self) -> str:
        result = ""
        if self.userinfo:
            result += f"{self.userinfo}@"
        result += self.host
        if self.port is not None:
            result += f":{self.port}"
        return result

    def scheme_(self, scheme: str) -> Uri:
        return replace(self, scheme=scheme)

    def userinfo_(self, userinfo: str) -> Uri:
        return replace(self, userinfo=userinfo)

    def host_(self, host: str) -> Uri:
        return replace(self, host=host)

    def port_(self, port: int | None) -> Uri:
        return replace(self, port=port)

    def path_(self, path: str) -> Uri:
        return replace(self, path=path)

    def query_string(self, query: str) -> Uri:
        return replace(self, query=query)

    def fragment_(self, fragment: str) -> Uri:
        return replace(self, fragment=fragment)

    def authority_(self, authority: str) -> Uri:
        userinfo, host, port = self._parse_authority(authority)
        return replace(self, userinfo=userinfo, host=host, port=port)

    def query_(self, name: str, value: str) -> Uri:
        params = _to_parameters(self.query)
        params.append((name, value))
        return self.query_string(_to_url_form_encoded(params))

    def remove_query(self, name: str) -> Uri:
        params = _to_parameters(self.query)
        filtered_params = [(k, v) for k, v in params if k != name]
        return self.query_string(_to_url_form_encoded(filtered_params))

    def remove_queries(self, prefix: str = "") -> Uri:
        params = _to_parameters(self.query)
        filtered_params = [(k, v) for k, v in params if not k.startswith(prefix)]
        return self.query_string(_to_url_form_encoded(filtered_params))

    def queries(self) -> list[tuple[str, str | None]]:
        return _to_parameters(self.query)

    def append_to_path(self, path_to_append: str) -> Uri:
        if not path_to_append:
            return self
        base_path = self.path.rstrip("/")
        append_path = path_to_append.lstrip("/")
        new_path = f"{base_path}/{append_path}" if base_path else f"/{append_path}"
        return self.path_(new_path)

    def __str__(self) -> str:
        result = ""

        if self.scheme:
            result += f"{self.scheme}:"

        authority = self.authority
        if authority:
            result += f"//{authority}"

        if authority and self.path and not self.path.startswith("/"):
            result += f"/{self.path}"
        else:
            result += self.path

        if self.query:
            result += f"?{self.query}"

        if self.fragment:
            result += f"#{self.fragment}"

        return result

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Uri):
            return NotImplemented
        return str(self) < str(other)
