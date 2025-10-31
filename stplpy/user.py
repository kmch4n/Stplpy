import requests
from typing import Dict, List, Optional, Any

from .exceptions import (
    APIError,
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError
)


class User:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "User-Agent": "Studyplus/101 CFNetwork/1474 Darwin/23.0.0",
            "Authorization": f"OAuth {token}"
        }

    def get_myself(self) -> Dict[str, Any]:
        url = "https://api.studyplus.jp/2/me"
        result = requests.get(url, headers=self.headers)
        if result.status_code == 200:
            return result.json()
        elif result.status_code in (401, 403):
            raise AuthenticationError(f"[{result.status_code}] Authentication failed")
        else:
            raise APIError(f"[{result.status_code}] Failed to get user profile", result.status_code)

    def get_user(self, user_name: str) -> Dict[str, Any]:
        url = f"https://api.studyplus.jp/2/users/{user_name}"
        result = requests.get(url, headers=self.headers)
        if result.status_code == 200:
            return result.json()
        elif result.status_code == 404:
            raise ResourceNotFoundError(f"User '{user_name}' not found")
        elif result.status_code in (401, 403):
            raise AuthenticationError(f"[{result.status_code}] Authentication failed")
        else:
            raise APIError(f"[{result.status_code}] Failed to get user '{user_name}'", result.status_code)

    def download_profile_picture(self, user_name: Optional[str] = None, output_file_name: str = "output.jpg") -> bool:
        if user_name is None:
            user_name = self.get_myself()["username"]
        try:
            profile_picture_url = self.get_user(user_name)["user_image_url"]
            data = requests.get(profile_picture_url).content
            with open(output_file_name, mode='wb') as f:
                f.write(data)
            return True
        except Exception as e:
            raise APIError(f"Failed to download profile picture: {str(e)}")

    def update_profile_picture(self, file_path: str) -> bool:
        url = "https://api.studyplus.jp/2/settings/profile_icon"
        try:
            with open(file_path, 'rb') as file:
                files = {
                    'image': ('image.jpg', file, 'image/jpeg')
                }
                result = requests.post(url, headers=self.headers, files=files)
        except FileNotFoundError:
            raise ValidationError(f"Profile picture file not found: {file_path}")

        if result.status_code == 204:
            return True
        elif result.status_code in (401, 403):
            raise AuthenticationError(f"[{result.status_code}] Authentication failed")
        else:
            raise APIError(f"[{result.status_code}] Failed to update profile picture", result.status_code)

    def follow_user(self, user_name: str) -> bool:
        data = {"username": user_name}
        url = "https://api.studyplus.jp/2/follows"
        result = requests.post(url, headers=self.headers, json=data)
        if result.status_code == 200:
            return True
        elif result.status_code == 404:
            raise ResourceNotFoundError(f"User '{user_name}' not found")
        elif result.status_code in (401, 403):
            raise AuthenticationError(f"[{result.status_code}] Authentication failed")
        else:
            raise APIError(f"[{result.status_code}] Failed to follow user '{user_name}'", result.status_code)

    def unfollow_user(self, user_name: str) -> bool:
        relationship_id = self.get_user(user_name)["user_relationship_id"]
        url = f"https://api.studyplus.jp/2/follows/{str(relationship_id)}"
        result = requests.delete(url, headers=self.headers)
        if result.status_code == 200:
            return True
        elif result.status_code == 404:
            raise ResourceNotFoundError(f"User relationship not found")
        elif result.status_code in (401, 403):
            raise AuthenticationError(f"[{result.status_code}] Authentication failed")
        else:
            raise APIError(f"[{result.status_code}] Failed to unfollow user '{user_name}'", result.status_code)

    def get_followees(self, target_id: str, limit: int = 10, header_less: bool = False) -> List[Dict[str, Any]]:
        count: int = 1
        results = []
        try:
            for _ in range(limit):
                url = f"https://api.studyplus.jp/2/users?followee={target_id}&page={count}&per_page=50&include_recent_record_seconds=t"
                count += 1
                if header_less:
                    result = requests.get(url, headers={})
                else:
                    result = requests.get(url, headers=self.headers)
                if result.status_code != 200:
                    continue
                for user in result.json()["users"]:
                    results.append(user)
            return results
        except Exception as e:
            raise APIError(f"Failed to get followees: {str(e)}")

    def get_followers(self, target_id: str, limit: int = 10, header_less: bool = False) -> List[Dict[str, Any]]:
        count: int = 1
        results = []
        try:
            for _ in range(limit):
                url = f"https://api.studyplus.jp/2/users?follower={target_id}&page={count}&per_page=50&include_recent_record_seconds=t"
                count += 1
                if header_less:
                    result = requests.get(url, headers={})
                else:
                    result = requests.get(url, headers=self.headers)
                if result.status_code != 200:
                    continue
                for user in result.json()["users"]:
                    results.append(user)
            return results
        except Exception as e:
            raise APIError(f"Failed to get followers: {str(e)}")
