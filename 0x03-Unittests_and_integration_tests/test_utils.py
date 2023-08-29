#!/usr/bin/env python3
""" Parameterize and patch as decorators """


import unittest
from fixtures import TEST_PAYLOAD
from typing import Dict
from parameterized import parameterized, parameterized_class
from requests import HTTPError
from client import GithubOrgClient
from unittest.mock import (
    patch,
    Mock,
    PropertyMock,
    MagicMock
)
from utils import get_json, access_nested_map, memoize


class TestGithubOrgClient(unittest.TestCase):
    """ Class for testing GithubOrgClient """
    @parameterized.expand([
        ('google', {'login': 'google'}),
        ('abc', {'login': 'abc'}),
    ])
    @patch('client.get_json')
    def test_org(self, test_org: str, resp: Dict, mocked_whyte: MagicMock) -> None:
        """ Test GithubOrgClient.org method """
        mocked_whyte.return_value = MagicMock(return_value=resp)
        whyte_class = GithubOrgClient(test_org)
        self.assertEqual(whyte_class.org(), resp)
        mocked_whyte.assert_called_once_with(
            'https://api.github.com/orgs/{}'.format(test_org)
        )

    @patch('client.GithubOrgClient._public_repos_url',
           new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org: MagicMock) -> None:
        """ Test GithubOrgClient._public_repos_url

        Args:
            mock_public_repos_url (MagicMock): [description]
        """
        mock_payload = {
            "repos_url": 'http://api.github.com/orgs/testorg/repos'}
        mock_org.return_value = mock_payload

        test_class = GithubOrgClient("testorg")
        result = test_class._public_repos_url()

        expected_url = 'https://api.github.com/orgs/testorg/repos'
        self.assertEqual(result, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get: MagicMock) -> None:
        """ Test GithubOrgClient.public_repos method """
        mock_payload = {
            'repos_url': 'https://api.github.com/repos/google/repos',
            'repos': [
                {
                    'id': 7697149,
                    'name': 'episodes.dart',
                    'private': False,
                    'owner': {
                        'login': 'google',
                        'id': 1342004,
                    },
                    'fork': False,
                    'url': 'https://api.github.com/repos/google/episodes.dart',
                    'created_at': '2013-01-19T00:31:37Z',
                    'updated_at': '2019-09-23T11:53:58Z',
                    'has_issues': True,
                    'forks': 22,
                    'default_branch': "master",
                },
                {
                    'id': 8566972,
                    'name': 'kratu',
                    'private': False,
                    'owner': {
                        'login': 'google',
                        'id': 1342004,
                    },
                    'fork': False,
                    'url': 'https://api.github.com/repos/google/kratu',
                    'created_at': '2013-03-04T22:52:33Z',
                    'updated_at': '2019-11-15T22:22:16Z',
                    'has_issues': True,
                    'forks': 32,
                    'default_branch': 'master',
                },
            ]
        }
        mock_get.return_value = mock_payload['repos']
        with patch.object(
            GithubOrgClient, '_public_repos_url',
                new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = mock_payload['repos_url']
            self.assertEqual(
                GithubOrgClient('google').public_repos(),
                [
                    'episodes.dart',
                    'kratu'
                ]
            )
            mock_public_repos_url.assert_called_once_with()
        mock_get.assert_called_once_with()

    @parameterized.expand([
        ({'license': {'key': 'my_license'}}, 'my_license', True),
        ({'license': {'key': 'other_license'}}, 'my_license', False),
    ])
    @patch('client.get_json')
    def test_has_license(self, repo: Dict, license_key: str,
                         expected: bool, mock_get: MagicMock) -> None:
        """ Test GithubOrgClient.has_license method """
        mock_payload = {
            'repos_url': 'https://api.github.com/orgs/google/repos',
            'repos': [repo]
        }
        mock_get.return_value = mock_payload['repos']
        with patch(
            'client.GithubOrgClient._public_repos_url',
                new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = mock_payload['repos_url']
            self.assertEqual(
                GithubOrgClient('google').has_license(license_key, repo),
                expected
            )
            mock_public_repos_url.assert_called_once_with()
        mock_get.assert_called_once_with(mock_payload['repos_url'])


if __name__ == '__main__':
    unittest.main()
