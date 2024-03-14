from .timeline import Timeline
from .user import User
import datetime
import json


class StudyPlus:
    def __init__(self, token: str):
        self.token = token
        self.user = User(token)
        self.timeline = Timeline(token)

    def log(self, text: str) -> None:
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}")

    # __________User__________
    def get_myself(self) -> json:
        return self.user.get_myself()

    def get_user(self, user_name: str) -> json:
        return self.user.get_user(user_name)

    def update_profile_picture(self, file_path: str) -> bool:
        return self.user.update_profile_picture(file_path)

    def follow_user(self, user_name: str) -> bool:
        return self.user.follow_user(user_name)

    def unfollow_user(self, user_name: str) -> bool:
        return self.user.unfollow_user(user_name)

    def get_followees(self, target_id: str, limit: int = 10, header_less: bool = False) -> list:
        return self.user.get_followees(target_id, limit, header_less)

    def get_followers(self, target_id: str, limit: int = 10, header_less: bool = False) -> list:
        return self.user.get_followers(target_id, limit, header_less)

    # __________Timeline__________
    def like_post(self, post_id: str) -> bool:
        return self.timeline.like_post(post_id)

    def unlike_post(self, post_id: str) -> bool:
        return self.timeline.unlike_post(post_id)

    def comment(self, post_id: str, text: str) -> bool:
        return self.timeline.comment(post_id, text)

    def post_study_record(self, material_code: str = None, duration: int = 0, comment: str = "", record_datetime: str = None) -> bool:
        return self.timeline.post_study_record(material_code, duration, comment, record_datetime)

    def delete_study_record(self, record_number: int) -> bool:
        return self.timeline.delete_study_record(record_number)

    def get_user_timeline(self, target_id: str, until: str = None) -> json:
        return self.timeline.get_user_timeline(target_id, until)

    def get_goal_timeline(self, target_id: str, until: str = None) -> json:
        return self.timeline.get_goal_timeline(target_id, until)

    def get_achievement_timeline(self, target_id: str, until: str = None) -> json:
        return self.timeline.get_achievement_timeline(target_id, until)

    def get_user_timelines(self, target_id: str, limit: int = 3) -> list:
        return self.timeline.get_user_timelines(target_id, limit)

    def get_goal_timelines(self, target_id: str, limit: int = 3) -> list:
        return self.timeline.get_goal_timelines(target_id, limit)

    def get_achievement_timelines(self, target_id: str, limit: int = 3) -> list:
        return self.timeline.get_achievement_timelines(target_id, limit)
