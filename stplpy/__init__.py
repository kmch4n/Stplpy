from .timeline import Timeline
from .user import User
import datetime


class StudyPlus:
    def __init__(self, token: str):
        self.token = token
        self.user = User(token)
        self.timeline = Timeline(token)

    def log(self, text: str):
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}")

    # __________User__________
    def get_myself(self):
        return self.user.get_myself()

    def get_user(self, user_name: str):
        return self.user.get_user(user_name)

    def follow_user(self, user_name: str):
        return self.user.follow_user(user_name)

    def unfollow_user(self, user_name: str):
        return self.user.unfollow_user(user_name)

    def get_followees(self, target_id: str, limit: int = 10, header_less: bool = False):
        return self.user.get_followees(target_id, limit, header_less)

    def get_followers(self, target_id: str, limit: int = 10, header_less: bool = False):
        return self.user.get_followers(target_id, limit, header_less)

    # __________Timeline__________
    def like_post(self, post_id: str):
        return self.timeline.like_post(post_id)

    def unlike_post(self, post_id: str):
        return self.timeline.unlike_post(post_id)

    def comment(self, post_id: str, text: str):
        return self.timeline.comment(post_id, text)

    def post_study_record(self, material_code: str = None, duration: int = 0, comment: str = "", record_datetime: str = None,):
        return self.timeline.post_study_record(material_code, duration, comment, record_datetime)

    def delete_study_record(self, record_number: int):
        return self.timeline.delete_study_record(record_number)

    def get_user_timeline(self, target_id: str, until: str = None):
        return self.timeline.get_user_timeline(target_id, until)

    def get_goal_timeline(self, target_id: str, until: str = None):
        return self.timeline.get_goal_timeline(target_id, until)

    def get_achievement_timeline(self, target_id: str, until: str = None):
        return self.timeline.get_achievement_timeline(target_id, until)

    def get_user_timelines(self, target_id: str, limit: int = 3):
        return self.timeline.get_user_timelines(target_id, limit)

    def get_goal_timelines(self, target_id: str, limit: int = 3):
        return self.timeline.get_goal_timelines(target_id, limit)

    def get_achievement_timelines(self, target_id: str, limit: int = 3):
        return self.timeline.get_achievement_timelines(target_id, limit)
