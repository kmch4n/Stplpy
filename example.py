from stplpy import StudyPlus
from dotenv import load_dotenv
import requests
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

toshin_profile_pic_url = toshin["user_image_url"]
file_name = 'toshin_profile_pic.jpg'
data = requests.get(toshin_profile_pic_url).content
with open(file_name, mode='wb') as f:
    f.write(data) # 東進のプロフィールurlをダウンロード
cl.update_profile_picture(file_path=file_name) # アイコンを指定した画像ファイルに変更
