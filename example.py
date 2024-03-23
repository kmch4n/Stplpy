from stplpy import StudyPlus
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv(".env")

cl = StudyPlus(os.environ["TOKEN"])

myself = cl.get_myself()
print(f'''userid : {myself["user_id"]}
username : {myself["username"]}
nickname : {myself["nickname"]}
follow : {myself["follow_count"]}
follower : {myself["follower_count"]}
''')

toshin_user_id = "545c0b9e9b0e47cb83ed560c5c08bd72"  # 東進ハイスクール 公式アカウント
toshin = cl.get_user(user_name=toshin_user_id)
print(f'''userid : {toshin["user_id"]}
username : {toshin["username"]}
nickname : {toshin["nickname"]}
follow : {toshin["follow_count"]}
follower : {toshin["follower_count"]}
''')

cl.follow_user(user_name=toshin_user_id)
cl.unfollow_user(user_name=toshin_user_id)

tl = cl.get_user_timeline(toshin_user_id)
post = cl.get_post_detail(tl["feeds"][0]["body_study_record"]["event_id"], include_like_users=True, include_comments=True)
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(post, f, indent=4, ensure_ascii=False)

cl.like_post(tl["feeds"][0]["body_study_record"]["event_id"])
cl.unlike_post(tl["feeds"][0]["body_study_record"]["event_id"])

target_1900 = "ASIN4010339179"  # ターゲット1900 教材id
duration = 60  # ここは秒数 10分の場合は600 1時間の場合は3600
cl.post_study_record(material_code=target_1900, duration=duration, comment="朝活", record_datetime="2000-01-01T00:00:00Z")
cl.delete_study_record(cl.get_user_timeline(myself["username"])["feeds"][0]["body_study_record"]["record_id"])

todai = "college-180"  # 東京大学
cl.like_post(
    cl.get_goal_timeline(target_id=todai)["feeds"][0]["body_study_record"]["event_id"]
)
cl.like_post(
    cl.get_achievement_timeline(target_id=todai)["feeds"][0]["body_study_achievement"]["event_id"]
)

cl.download_profile_picture(user_name=toshin["username"], output_file_name="toshin.jpg")  # アイコンを名前を指定して保存
cl.update_profile_picture(file_path="toshin.jpg")  # アイコンを指定した画像ファイルに変更
