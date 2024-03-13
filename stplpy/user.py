import requests
import json


class User:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "User-Agent": "Studyplus/101 CFNetwork/1474 Darwin/23.0.0",
            "Authorization": f"OAuth {token}"
        }

    def get_myself(self):
        url = "https://api.studyplus.jp/2/me"
        result = requests.get(url, headers=self.headers)
        if result.status_code == 200:
            return result.json()
        else:
            raise ValueError(f"[{result.status_code}] failed to get_myself :/")

    def get_user(self, user_name: str) -> json:
        url = f"https://api.studyplus.jp/2/users/{user_name}"
        result = requests.get(url, headers=self.headers)
        if result.status_code == 200:
            return result.json()
        else:
            raise ValueError(f"[{result.status_code}] failed to get_user :/")

    def follow_user(self, user_name: str) -> bool:
        data = {"username": user_name}
        url = "https://api.studyplus.jp/2/follows"
        result = requests.post(url, headers=self.headers, json=data)
        if result.status_code == 200:
            return True
        else:
            raise ValueError(
                f"[{result.status_code}] failed to follow user :/")

    def unfollow_user(self, user_name: str) -> bool:
        relationship_id = self.get_user(user_name)["user_relationship_id"]
        url = f"https://api.studyplus.jp/2/follows/{str(relationship_id)}"
        result = requests.delete(url, headers=self.headers)
        if result.status_code == 200:
            return True
        else:
            raise ValueError(
                f"[{result.status_code}] failed to unfollow user :/")

    def get_followees(self, target_id: str, limit: int = 10, header_less: bool = False) -> list:
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
            raise Exception(e)

    def get_followers(self, target_id: str, limit: int = 10, header_less: bool = False):
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
            raise Exception(e)
