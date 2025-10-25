from __future__ import annotations

import pytest
from http4py.core import Uri


class TestUriStringRepresentation:
    """Test Uri string representation matches http4k behavior."""

    def test_parsing_full_uri(self) -> None:
        """Test parsing a full URI with all components."""
        value = "http://user:pass@host:1234/some/path?q1=v1&q2=v2#abc"
        uri = Uri.of(value)

        assert uri.scheme == "http"
        assert uri.userinfo == "user:pass"
        assert uri.host == "host"
        assert uri.port == 1234
        assert uri.path == "/some/path"
        assert uri.query == "q1=v1&q2=v2"
        assert uri.fragment == "abc"
        assert str(uri) == value

    def test_creating_full_uri_by_hand(self) -> None:
        """Test building a URI using fluent API."""
        uri = (
            Uri()
            .scheme_("https")
            .userinfo_("user:pass")
            .host_("example.com")
            .port_(1234)
            .fragment_("bob")
            .path_("/a/b/c")
            .query_("foo", "bar")
        )

        expected = "https://user:pass@example.com:1234/a/b/c?foo=bar#bob"
        assert str(uri) == expected

    def test_handles_no_prefixed_slash_in_path(self) -> None:
        """Test that paths without leading slash get prefixed when authority present."""
        uri = Uri().scheme_("https").host_("example.com").port_(1234).path_("a/b/c")  # No leading slash

        expected = "https://example.com:1234/a/b/c"
        assert str(uri) == expected

    def test_equality_for_round_tripping(self) -> None:
        """Test that parsing and stringifying gives identical results."""
        original = "path"
        assert Uri.of(original) == Uri.of(str(Uri.of(original)))

    def test_can_parse_minimal_uri(self) -> None:
        """Test parsing minimal URI with just scheme and host."""
        value = "http://host"
        uri = Uri.of(value)

        assert uri.scheme == "http"
        assert uri.host == "host"
        assert uri.userinfo == ""
        assert uri.port is None
        assert uri.fragment == ""
        assert uri.path == ""
        assert uri.query == ""
        assert str(uri) == value

    def test_handles_empty_uri(self) -> None:
        """Test that empty URI remains empty."""
        assert str(Uri.of("")) == ""

    def test_string_representation_cases(self) -> None:
        """Test various URI string representation cases."""
        test_cases = [
            # Basic paths
            ("/", "/"),
            ("/api/users", "/api/users"),
            ("/path/to/resource", "/path/to/resource"),
            # Paths with queries
            ("/api/users?active=true", "/api/users?active=true"),
            ("/search?q=hello%20world&limit=10", "/search?q=hello%20world&limit=10"),
            ("/?search=test", "/?search=test"),
            # Paths with fragments
            ("/docs#section1", "/docs#section1"),
            ("/#top", "/#top"),
            # Complex combinations
            ("/api/users?active=true&sort=name#results", "/api/users?active=true&sort=name#results"),
            # Encoded paths
            ("/users/123/files/my%20document.pdf", "/users/123/files/my%20document.pdf"),
            # Query only
            ("?search=test", "?search=test"),
            # Fragment only
            ("#section", "#section"),
            # Full URLs
            ("http://example.com/path?query=value#fragment", "http://example.com/path?query=value#fragment"),
            ("https://user:pass@host:8080/api?token=abc#results", "https://user:pass@host:8080/api?token=abc#results"),
        ]

        for uri_string, expected in test_cases:
            uri = Uri.of(uri_string)
            result = str(uri)
            assert result == expected, f"Failed for {uri_string}: got {result}, expected {expected}"

    def test_authority_property(self) -> None:
        """Test authority property construction."""
        # No userinfo, no port
        uri = Uri().host_("example.com")
        assert uri.authority == "example.com"

        # With port
        uri = Uri().host_("example.com").port_(8080)
        assert uri.authority == "example.com:8080"

        # With userinfo
        uri = Uri().userinfo_("user:pass").host_("example.com")
        assert uri.authority == "user:pass@example.com"

        # With all
        uri = Uri().userinfo_("user:pass").host_("example.com").port_(8080)
        assert uri.authority == "user:pass@example.com:8080"


class TestUriParsing:
    """Test Uri parsing functionality."""

    def test_parse_scheme_only(self) -> None:
        """Test parsing URI with scheme only."""
        uri = Uri.of("http:")
        assert uri.scheme == "http"
        assert uri.host == ""
        assert uri.path == ""

    def test_parse_authority_variations(self) -> None:
        """Test parsing different authority formats."""
        # Host only
        uri = Uri.of("//example.com")
        assert uri.host == "example.com"
        assert uri.userinfo == ""
        assert uri.port is None

        # Host with port
        uri = Uri.of("//example.com:8080")
        assert uri.host == "example.com"
        assert uri.port == 8080

        # Userinfo with host
        uri = Uri.of("//user@example.com")
        assert uri.userinfo == "user"
        assert uri.host == "example.com"

        # Full authority
        uri = Uri.of("//user:pass@example.com:8080")
        assert uri.userinfo == "user:pass"
        assert uri.host == "example.com"
        assert uri.port == 8080

    def test_parse_invalid_authority_raises_error(self) -> None:
        """Test that invalid authority raises ValueError."""
        with pytest.raises(ValueError, match="Invalid authority"):
            Uri.of("http://::")


class TestUriBuilderPattern:
    """Test Uri builder pattern functionality."""

    def test_builder_methods_return_new_instances(self) -> None:
        """Test that builder methods return new Uri instances."""
        original = Uri()
        modified = original.scheme_("https")

        assert original is not modified
        assert original.scheme == ""
        assert modified.scheme == "https"

    def test_query_builder_methods(self) -> None:
        """Test query manipulation methods."""
        uri = Uri().path_("/api").query_("active", "true").query_("limit", "10")

        assert "active=true" in uri.query
        assert "limit=10" in uri.query
        assert str(uri) == "/api?active=true&limit=10"

    def test_remove_query_methods(self) -> None:
        """Test query removal methods."""
        uri = Uri().path_("/api").query_("active", "true").query_("limit", "10").query_("sort", "name")

        # Remove specific query
        uri_without_limit = uri.remove_query("limit")
        assert "limit" not in uri_without_limit.query
        assert "active=true" in uri_without_limit.query

        # Remove queries with prefix
        uri_with_prefixed = uri.query_("api_key", "secret").query_("api_version", "v1")
        uri_without_api = uri_with_prefixed.remove_queries("api_")
        assert "api_key" not in uri_without_api.query
        assert "api_version" not in uri_without_api.query
        assert "active=true" in uri_without_api.query

    def test_path_append_method(self) -> None:
        """Test path appending functionality."""
        base = Uri().path_("/api")

        # Append path segment
        extended = base.append_to_path("users")
        assert extended.path == "/api/users"

        # Append with leading slash
        extended2 = base.append_to_path("/users")
        assert extended2.path == "/api/users"

        # Append to root
        root = Uri().path_("/")
        extended3 = root.append_to_path("api")
        assert extended3.path == "/api"


class TestUriQueries:
    """Test Uri query parameter handling."""

    def test_queries_method_returns_parameters(self) -> None:
        """Test that queries() returns list of parameter tuples."""
        uri = Uri.of("/api?active=true&limit=10&sort=")
        queries = uri.queries()

        assert ("active", "true") in queries
        assert ("limit", "10") in queries
        assert ("sort", "") in queries

    def test_empty_query_returns_empty_list(self) -> None:
        """Test that empty query returns empty list."""
        uri = Uri.of("/api")
        assert uri.queries() == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
