#!/usr/bin/env python3
""" Authentication module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if auth is required
        """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) < 1:
            return True

        normalized_path = path.rstrip('/') + '/'
        for excluded_path in excluded_paths:
            if normalized_path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Checks authorisatin header
        """
        if request is None:
            return None

        if request.headers.get('Authorization') is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get current user
        """
        return None
