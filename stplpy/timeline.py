from datetime import datetime
import requests
import random
import string
import json


class Timeline:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "User-Agent": "Studyplus/101 CFNetwork/1474 Darwin/23.0.0",
            "Authorization": f"OAuth {token}"
        }

    def create_token(self, n: int = 10):
        randlst = [
            random.choice(string.ascii_letters + string.digits) for i in range(n)
        ]
        return "".join(randlst)

    def like_post(self, post_id: str) -> bool:
        url = f"https://api.studyplus.jp/2/timeline_events/{post_id}/likes/like"
        result = requests.post(url, headers=self.headers)
        if result.status_code == 200:
            return True
        else:
            raise ValueError(f"[{result.status_code}] failed to like post :/")

    def unlike_post(self, post_id: str) -> bool:
        url = f"https://api.studyplus.jp/2/timeline_events/{post_id}/likes/withdraw"
        result = requests.post(url, headers=self.headers)
        if result.status_code == 200:
            return True
        else:
            raise ValueError(f"[{result.status_code}] failed to unlike post :/")

    def comment(self, post_id: str, text: str) -> bool:
        param = {"post_token": "NONE", "comment": text}
        url = f"https://api.studyplus.jp/2/timeline_events/{post_id}/comments"
        result = requests.post(url, headers=self.headers, json=param)
        if result.status_code == 200:
            return True
        else:
            raise ValueError(f"[{result.status_code}] failed to comment :/")

    def post_study_record(self, material_code: str = None, duration: int = 0, comment: str = "", record_datetime: str = None,) -> bool:
        if record_datetime is None:
            record_datetime = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        data = {
            "study_source_type": "studyplus",
            "duration": duration,
            "record_datetime": record_datetime,
            "comment": comment,
            "post_token": self.create_token(),
        }
        if material_code:
            data["material_code"] = material_code
        url = "https://api.studyplus.jp/2/study_records"
        result = requests.post(url, headers=self.headers, json=data)
        if result.status_code == 200:
            return True
        else:
            raise ValueError(f"[{result.status_code}] failed to post study record :/")

    def delete_study_record(self, record_number: int):
        url = f"https://api.studyplus.jp/2/study_records/{str(record_number)}"
        result = requests.delete(url, headers=self.headers)
        if result.status_code == 200:
            return result.json()
        else:
            raise ValueError(f"[{result.status_code}] failed to delete study record :/")

    def get_user_timeline(self, target_id: str, until: str = None) -> json:
        if until is not None:
            url = f"https://api.studyplus.jp/2/timeline_feeds/user/{target_id}?until={until}"
        else:
            url = f"https://api.studyplus.jp/2/timeline_feeds/user/{target_id}"
        result = requests.get(url, headers=self.headers)
        if result.status_code == 200:
            return result.json()
        else:
            raise ValueError(f"[{result.status_code}] failed to get user timeline :/")

    def get_goal_timeline(self, target_id: str, until: str = None) -> json:
        if until is not None:
            url = f"https://api.studyplus.jp/2/timeline_feeds/study_goal/{target_id}?until={until}"
        else:
            url = f"https://api.studyplus.jp/2/timeline_feeds/study_goal/{target_id}"
        result = requests.get(url, headers=self.headers)
        if result.status_code == 200:
            return result.json()
        else:
            raise ValueError(f"[{result.status_code}] failed to get goal timeline :/")

    def get_achievement_timeline(self, target_goal: str = None, until: str = None) -> json:
        if target_goal is None:
            if until is not None:
                url = f"https://api.studyplus.jp/2/study_achievements/feeds?until={until}"
            else:
                url = f"https://api.studyplus.jp/2/study_achievements/feeds"
        else:
            if until is not None:
                url = f"https://api.studyplus.jp/2/study_achievements/feeds/study_goal/{
                    target_goal}?until={until}"
            else:
                url = f"https://api.studyplus.jp/2/study_achievements/feeds/study_goal/{
                    target_goal}"
        result = requests.get(url, headers=self.headers)
        if result.status_code == 200:
            return result.json()
        else:
            raise ValueError(f"[{result.status_code}] failed to get achievement timeline :/")

    def get_user_timelines(self, target_id: str, limit: int = 3) -> json:
        results = []
        until = None
        for _ in range(limit):
            if until is not None:
                result = self.get_user_timeline(target_id, until)
            else:
                result = self.get_user_timeline(target_id)
            for event in result["feeds"]:
                results.append(event)
            if "next" not in result:
                break
            until = result["next"]
        return results

    def get_goal_timelines(self, target_id: str, limit: int = 3) -> json:
        results = []
        until = None
        for _ in range(limit):
            if until is not None:
                result = self.get_goal_timeline(target_id, until)
            else:
                result = self.get_goal_timeline(target_id)
            for event in result["feeds"]:
                results.append(event)
            if "next" not in result:
                continue
            until = result["next"]
        return results

    def get_achievement_timelines(self, target_id: str, limit: int = 3) -> json:
        results = []
        until = None
        for _ in range(limit):
            if until is not None:
                result = self.get_achievement_timeline(target_id, until)
            else:
                result = self.get_achievement_timeline(target_id)
            for event in result["feeds"]:
                results.append(event)
            if "next" not in result:
                continue
            until = result["next"]
        return results
