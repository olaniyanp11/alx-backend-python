#!/usr/bin/env python3
from typing import Mapping, Tuple, Union, Any, Type
import unittest
from utils import access_nested_map
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """ Parameterize a unit test"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
            self,
            nested_map: Mapping,
            path: Tuple[int, str],
            expected: Union[Mapping, int]
            ) -> None:
        ''' Parameterize a unit test'''
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
        ])
    def test_access_nested_map_exception(
            self,
            nested_map: Mapping[Any, Any],
            path: Tuple[str],
            expected: Type[Exception]
            ) -> None:
        ''' Parameterize a unit test'''
        with self.assertRaises(expected):
            access_nested_map(nested_map, path)
