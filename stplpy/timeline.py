from datetime import datetime
import json
import random
import string

import requests
from requests.exceptions import HTTPError


class Timeline:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "User-Agent": "Studyplus/101 CFNetwork/1474 Darwin/23.0.0",
            "Authorization": f"OAuth {token}"
        }

    def create_token(self, n: int = 10) -> str:
        randlst = [
            random.choice(string.ascii_letters + string.digits) for i in range(n)
        ]
        return "".join(randlst)

    def get_post_detail(self, post_id: str, include_like_users: bool = False, like_user_count: int = 100, include_comments: bool = False, comment_count: int = 100) -> json:
        url = f"https://api.studyplus.jp/2/timeline_events/{post_id}"
        if include_like_users:
            url += f"?include_like_users=t&like_user_count={str(like_user_count)}"
        if include_comments:
            if include_like_users:
                url += f"&include_comments=t&comment_count={str(comment_count)}"
            else:
                url += f"?include_comments=t&comment_count={str(comment_count)}"
        try:
            result = requests.get(url, headers=self.headers)
            result.raise_for_status()
            return result.json()
        except HTTPError as http_err:
            raise Exception(f"[{result.status_code}] Failed to get post detail : {http_err}") from http_err

    def like_post(self, post_id: str) -> bool:
        url = f"https://api.studyplus.jp/2/timeline_events/{post_id}/likes/like"
        try:
            result = requests.post(url, headers=self.headers)
            result.raise_for_status()
            return True
        except HTTPError as http_err:
            raise Exception(f"[{result.status_code}] Failed to like post : {http_err}") from http_err

    def unlike_post(self, post_id: str) -> bool:
        url = f"https://api.studyplus.jp/2/timeline_events/{post_id}/likes/withdraw"
        try:
            result = requests.post(url, headers=self.headers)
            result.raise_for_status()
            return True
        except HTTPError as http_err:
            raise Exception(f"[{result.status_code}] Failed to unlike post : {http_err}") from http_err

    def comment(self, post_id: str, text: str) -> bool:
        param = {"post_token": "NONE", "comment": text}
        url = f"https://api.studyplus.jp/2/timeline_events/{post_id}/comments"
        try:
            result = requests.post(url, headers=self.headers, json=param)
            result.raise_for_status()
            return True
        except HTTPError as http_err:
            raise Exception(f"[{result.status_code}] Failed to comment on post : {http_err}") from http_err

    def post_study_record(self, material_code: str = None, duration: int = 0, comment: str = "", record_datetime: str = None) -> bool:
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
        try:
            result = requests.post(url, headers=self.headers, json=data)
            result.raise_for_status()
            return True
        except HTTPError as http_err:
            raise Exception(f"[{result.status_code}] Failed to post study record : {http_err}") from http_err

    def delete_study_record(self, record_number: int):
        url = f"https://api.studyplus.jp/2/study_records/{str(record_number)}"
        try:
            result = requests.delete(url, headers=self.headers)
            result.raise_for_status()
            return result.json()
        except HTTPError as http_err:
            raise Exception(f"[{result.status_code}] Failed to delete study record : {http_err}") from http_err

    def get_user_timeline(self, target_id: str, until: str = None):
        if until is not None:
            url = f"https://api.studyplus.jp/2/timeline_feeds/user/{target_id}?until={until}"
        else:
            url = f"https://api.studyplus.jp/2/timeline_feeds/user/{target_id}"
        try:
            result = requests.get(url, headers=self.headers)
            result.raise_for_status()
            return result.json()
        except HTTPError as http_err:
            raise Exception(f"[{result.status_code}] Failed to get user timeline : {http_err}") from http_err

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
        try:
            result = requests.get(url, headers=self.headers)
            result.raise_for_status()
            return result.json()
        except HTTPError as http_err:
            raise Exception(f"[{result.status_code}] Failed to get achievement timeline : {http_err}") from http_err

    def get_user_timelines(self, target_id: str, limit: int = 3) -> list:
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

    def get_goal_timelines(self, target_id: str, limit: int = 3) -> list:
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

    def get_achievement_timelines(self, target_id: str, limit: int = 3) -> list:
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
