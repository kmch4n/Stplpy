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

    def get_user(self, user_name):
        url = f"https://api.studyplus.jp/2/users/{user_name}"
        result = requests.get(url, headers=self.headers)
        if result.status_code == 200:
            return result.json()
        else:
            raise ValueError(f"[{result.status_code}] failed to get_user :/")

    def download_profile_picture(self, user_name, output_file_name):
        if user_name is None:
            user_name = self.get_myself()["username"]
        try:
            profile_picture_url = self.get_user(user_name)["user_image_url"]
            data = requests.get(profile_picture_url).content
            with open(output_file_name, mode='wb') as f:
                f.write(data)
            return True
        except Exception as e:
            raise Exception(e)

    def update_profile_picture(self, file_path):
        url = "https://api.studyplus.jp/2/settings/profile_icon"
        with open(file_path, 'rb') as file:
            files = {
                'image': ('image.jpg', file, 'image/jpeg')
            }
            result = requests.post(url, headers=self.headers, files=files)
        if result.status_code == 204:
            return True
        else:
            raise ValueError(f"[{result.status_code}] failed to update_profile_picture :/")

    def follow_user(self, user_name):
        data = {"username": user_name}
        url = "https://api.studyplus.jp/2/follows"
        result = requests.post(url, headers=self.headers, json=data)
        if result.status_code == 200:
            return True
        else:
            raise ValueError(
                f"[{result.status_code}] failed to follow user :/")

    def unfollow_user(self, user_name):
        relationship_id = self.get_user(user_name)["user_relationship_id"]
        url = f"https://api.studyplus.jp/2/follows/{str(relationship_id)}"
        result = requests.delete(url, headers=self.headers)
        if result.status_code == 200:
            return True
        else:
            raise ValueError(
                f"[{result.status_code}] failed to unfollow user :/")

    def get_followees(self, target_id, limit, header_less):
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

    def get_followers(self, target_id, limit, header_less):
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
