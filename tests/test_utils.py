from openapi_tester.utils import (
    get_required_keys,
    merge_objects,
    serialize_schema_section_data,
)
from tests.utils import sort_object


def test_documentation_error_sort_data_type():
    assert sort_object([1, 3, 2]) == [1, 2, 3]  # list
    assert sort_object({"1", "3", "2"}) == {"1", "2", "3"}  # set
    assert sort_object({"1": "a", "3": "a", "2": "a"}) == {
        "1": "a",
        "2": "a",
        "3": "a",
    }  # dict

    # Test sort failure scenario - expect the method to succeed and default to no reordering
    assert sort_object(["1", {}, []]) == ["1", {}, []]


def test_merge_objects():
    object_1 = {
        "type": "object",
        "required": ["key1"],
        "properties": {"key1": {"type": "string"}},
    }
    object_2 = {
        "type": "object",
        "required": ["key2"],
        "properties": {"key2": {"type": "string"}},
    }
    test_schemas = [
        object_1,
        object_2,
    ]
    expected = {
        "type": "object",
        "required": ["key1", "key2"],
        "properties": {"key1": {"type": "string"}, "key2": {"type": "string"}},
    }
    assert sort_object(merge_objects(test_schemas)) == sort_object(expected)


def test_serialize_schema_section_data():
    data = {
        "type": "object",
        "required": ["key1", "key2"],
        "properties": {"key1": {"type": "string"}, "key2": {"type": "string"}},
    }
    serialized_data = serialize_schema_section_data(data=data)
    assert serialized_data == (
        "{\n  "
        '"type": "object",'
        '\n  "required": [\n    "key1",\n    "key2"\n  ],\n  '
        '"properties": {\n'
        '    "key1": {\n      "type": "string"\n    },\n'
        '    "key2": {\n      "type": "string"\n    }\n'
        "  }"
        "\n}"
    )


def test_get_required_keys():
    # given
    schema_section = {
        "type": "object",
        "required": ["key1", "key2"],
        "properties": {"key1": {"type": "string"}, "key2": {"type": "string"}},
    }
    read_only_props = []
    write_only_props = []
    http_message = "response"

    # when
    required_keys = get_required_keys(
        schema_section=schema_section,
        http_message=http_message,
        read_only_props=read_only_props,
        write_only_props=write_only_props,
    )

    # then
    assert required_keys == ["key1", "key2"]


def test_get_required_keys_request_with_read_only_field():
    # given
    schema_section = {
        "type": "object",
        "required": ["key1", "key2"],
        "properties": {"key1": {"type": "string"}, "key2": {"type": "string"}},
        "readOnly": ["key2"],
    }
    read_only_props = ["key2"]
    write_only_props = []

    http_message = "request"

    # when
    required_keys = get_required_keys(
        schema_section=schema_section,
        http_message=http_message,
        read_only_props=read_only_props,
        write_only_props=write_only_props,
    )

    # then
    assert required_keys == ["key1"]


def test_get_required_keys_response_with_write_only_field():
    # given
    schema_section = {
        "type": "object",
        "required": ["key1", "key2"],
        "properties": {"key1": {"type": "string"}, "key2": {"type": "string"}},
        "writeOnly": ["key2"],
    }
    write_only_props = ["key2"]
    read_only_props = []
    http_message = "response"

    # when
    required_keys = get_required_keys(
        schema_section=schema_section,
        http_message=http_message,
        write_only_props=write_only_props,
        read_only_props=read_only_props,
    )

    # then
    assert required_keys == ["key1"]
