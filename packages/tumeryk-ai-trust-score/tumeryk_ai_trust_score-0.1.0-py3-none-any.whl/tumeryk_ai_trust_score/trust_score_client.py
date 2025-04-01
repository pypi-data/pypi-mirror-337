# Copyright Tumeryk 2024

import os
import requests
from requests.exceptions import RequestException
from typing import Dict, Any, Optional

class TumerykTrustScoreClient:
    """API Client for Tumeryk AI Trust Score"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, base_url: str = None, auth_url: str = None):
        if not hasattr(self, '_initialized'):
            self.auth_url = auth_url or os.getenv("TUMERYK_AUTH_URL", "https://chat.tmryk.com")
            self.base_url = base_url or os.getenv("TUMERYK_BASE_URL", "https://trust-score.tmryk.com/")
            self.token = None
            self.session = requests.Session()
            self._auto_login()
            self._initialized = True

    def _auto_login(self):
        """Automatically login if environment variables are available."""
        username = os.getenv("TUMERYK_USERNAME")
        password = os.getenv("TUMERYK_PASSWORD")
        
        if username and password:
            try:
                self.login(username, password)
            except RequestException as err:
                print(f"Auto-login failed: {err}")

    def login(self, username: str, password: str):
        """Authenticate and store access token."""
        username = username or os.getenv("TUMERYK_USERNAME")
        password = password or os.getenv("TUMERYK_PASSWORD")

        if not username or not password:
            raise ValueError("Username and password must be provided either as arguments or environment variables.")

        payload = {"grant_type": "password", "username": username, "password": password}
        response = self.session.post(f"{self.auth_url}/auth/token", data=payload)
        response.raise_for_status()
        response_data = response.json()

        if "access_token" in response_data:
            self.token = response_data["access_token"]
        else:
            print("Login failed, no access token in response")
        return response_data

    def _get_headers(self):
        """Helper method to get the headers including authorization."""
        if not self.token:
            self._auto_login()
            if not self.token:
                raise ValueError("You must login first before making API calls")
        return {"Authorization": f"Bearer {self.token}"}

    def get_trust_scores(self) -> Dict[str, Any]:
        """
        Get trust scores for all available models.
        
        Returns:
            Dict containing the trust scores for all models, including total scores
            and category-specific scores for each model.
        """
        try:
            headers = self._get_headers()
            response = self.session.get(
                f"{self.base_url}/calculate_model_scores",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except RequestException as err:
            print(f"Request failed: {err}")
            return {"error": f"Request failed: {err}"}
        except Exception as err:
            print(f"An unexpected error occurred: {err}")
            return {"error": f"An unexpected error occurred: {err}"}

    def get_base_url(self) -> str:
        """Get the current base URL."""
        return self.base_url

    def set_base_url(self, base_url: str):
        """Set a new base URL."""
        self.base_url = base_url

    def get_auth_url(self) -> str:
        """Get the current auth URL."""
        return self.auth_url

    def set_auth_url(self, auth_url: str):
        """Set a new auth URL."""
        self.auth_url = auth_url

    def set_token(self, token: str):
        """Set a new token directly"""
        self.token = token

# Create a singleton instance
trust_score = TumerykTrustScoreClient() 