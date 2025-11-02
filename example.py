"""
Stplpy Example Script

This script demonstrates the various features of the Stplpy library.
Each section shows different API functionalities with proper error handling.

Note: Operations that modify data (follow/unfollow, post/delete) are commented out
      for safety. Uncomment them carefully when you want to test those features.
"""

import json
import os
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from stplpy import StudyPlus
from stplpy.exceptions import (
    AuthenticationError,
    ResourceNotFoundError,
    RateLimitError,
    APIError
)

# ==============================================================================
# Configuration
# ==============================================================================

# Sample user IDs and material codes for testing
SAMPLE_USER_ID = "545c0b9e9b0e47cb83ed560c5c08bd72"  # 東進ハイスクール公式
SAMPLE_MATERIAL = "ASIN4010339179"  # ターゲット1900
SAMPLE_GOAL = "college-180"  # 東京大学

# Output settings
OUTPUT_JSON_FILE = "data.json"
OUTPUT_IMAGE_FILE = "profile_picture.jpg"


# ==============================================================================
# Utility Functions
# ==============================================================================

def print_section(title: str) -> None:
    """Print a section header for better readability."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def safe_api_call(func, *args, **kwargs) -> Optional[Any]:
    """
    Safely execute an API call with error handling.

    Args:
        func: The API function to call
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function

    Returns:
        The result of the API call, or None if an error occurred
    """
    try:
        return func(*args, **kwargs)
    except AuthenticationError:
        print("❌ Authentication failed. Please check your TOKEN.")
        return None
    except ResourceNotFoundError:
        print("❌ Resource not found.")
        return None
    except RateLimitError:
        print("❌ Rate limit exceeded. Please wait before trying again.")
        return None
    except APIError as e:
        print(f"❌ API Error: {e.status_code} - {e.message}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


# ==============================================================================
# Feature Demonstrations
# ==============================================================================

def demo_user_information(cl: StudyPlus) -> None:
    """Demonstrate user information retrieval."""
    print_section("1. User Information")

    # Get own user information
    print("\n📱 Getting your profile information...")
    myself = safe_api_call(cl.get_myself)
    if myself:
        print(f"""
✅ Your Profile:
   User ID:  {myself['user_id']}
   Username: {myself['username']}
   Nickname: {myself['nickname']}
   Following: {myself['follow_count']}
   Followers: {myself['follower_count']}
        """)

    # Get another user's information
    print(f"\n📱 Getting user information for: {SAMPLE_USER_ID}")
    user = safe_api_call(cl.get_user, user_name=SAMPLE_USER_ID)
    if user:
        print(f"""
✅ User Profile:
   User ID:  {user['user_id']}
   Username: {user['username']}
   Nickname: {user['nickname']}
   Following: {user['follow_count']}
   Followers: {user['follower_count']}
        """)


def demo_timeline_operations(cl: StudyPlus) -> None:
    """Demonstrate timeline retrieval and interaction."""
    print_section("2. Timeline Operations")

    # Get followee timeline
    print("\n📰 Getting followee timeline...")
    my_tl = safe_api_call(cl.get_followee_timeline)
    if my_tl and my_tl.get('feeds'):
        print(f"✅ Retrieved {len(my_tl['feeds'])} posts from your timeline")

        # Display first few posts
        print("\n📝 Recent posts:")
        for i, feed in enumerate(my_tl['feeds'][:3], 1):
            if feed.get('feed_type') == 'study_record':
                record = feed.get('body_study_record', {})
                print(f"   {i}. {record.get('material_title', 'N/A')} "
                      f"({record.get('duration', 0)} seconds)")

        # Like posts (commented out for safety)
        # print("\n👍 Liking recent posts...")
        # for n in range(min(3, len(my_tl['feeds']))):
        #     if my_tl['feeds'][n]['feed_type'] == 'study_record':
        #         event_id = my_tl['feeds'][n]['body_study_record']['event_id']
        #         result = safe_api_call(cl.like_post, event_id)
        #         if result:
        #             print(f"   ✅ Liked post {n+1}")

    # Get user timeline
    print(f"\n📰 Getting user timeline for: {SAMPLE_USER_ID}")
    user_tl = safe_api_call(cl.get_user_timeline, SAMPLE_USER_ID)
    if user_tl and user_tl.get('feeds'):
        print(f"✅ Retrieved {len(user_tl['feeds'])} posts from user timeline")


def demo_post_operations(cl: StudyPlus) -> None:
    """Demonstrate post detail retrieval and interactions."""
    print_section("3. Post Operations")

    # Get user timeline first
    print(f"\n📰 Getting timeline for post operations...")
    user_tl = safe_api_call(cl.get_user_timeline, SAMPLE_USER_ID)

    if user_tl and user_tl.get('feeds') and len(user_tl['feeds']) > 0:
        first_feed = user_tl['feeds'][0]

        if first_feed.get('feed_type') == 'study_record':
            event_id = first_feed['body_study_record']['event_id']

            # Get post detail
            print(f"\n📄 Getting detailed information for post {event_id}...")
            post = safe_api_call(
                cl.get_post_detail,
                event_id,
                include_like_users=True,
                include_comments=True
            )

            if post:
                print("✅ Post details retrieved successfully")

                # Save to JSON
                print(f"\n💾 Saving post details to {OUTPUT_JSON_FILE}...")
                try:
                    with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as f:
                        json.dump(post, f, indent=4, ensure_ascii=False)
                    print(f"✅ Saved to {OUTPUT_JSON_FILE}")
                except Exception as e:
                    print(f"❌ Failed to save JSON: {e}")

            # Like/unlike post (commented out for safety)
            # print(f"\n👍 Testing like/unlike for post {event_id}...")
            # if safe_api_call(cl.like_post, event_id):
            #     print("   ✅ Post liked")
            # if safe_api_call(cl.unlike_post, event_id):
            #     print("   ✅ Post unliked")

            # Comment operations (commented out for safety)
            # print(f"\n💬 Testing comment operations for post {event_id}...")
            # comment = safe_api_call(cl.send_comment, event_id, "👍")
            # if comment:
            #     print("   ✅ Comment sent")
            #     comment_id = comment.get('coment_id')  # Note: typo in API response
            #     if comment_id:
            #         if safe_api_call(cl.unsend_comment, event_id, comment_id):
            #             print("   ✅ Comment deleted")


def demo_study_record_operations(cl: StudyPlus, myself: Optional[Dict] = None) -> None:
    """Demonstrate study record posting and deletion."""
    print_section("4. Study Record Operations")

    # Post study record (commented out for safety)
    # print(f"\n📝 Posting a study record...")
    # print(f"   Material: {SAMPLE_MATERIAL}")
    # print(f"   Duration: 60 seconds (1 minute)")
    # record = safe_api_call(
    #     cl.post_study_record,
    #     material_code=SAMPLE_MATERIAL,
    #     duration=60,
    #     comment="Example study record",
    #     record_datetime="2000-01-01T00:00:00Z"
    # )
    # if record:
    #     print("   ✅ Study record posted successfully")
    #     record_id = record.get('record_id')
    #
    #     # Delete the record we just posted
    #     if record_id:
    #         print(f"\n🗑️  Deleting study record {record_id}...")
    #         if safe_api_call(cl.delete_study_record, record_id):
    #             print("   ✅ Study record deleted successfully")

    print("\n⚠️  Study record operations are commented out for safety.")
    print("    Uncomment lines in demo_study_record_operations() to test.")


def demo_follow_operations(cl: StudyPlus) -> None:
    """Demonstrate follow/unfollow operations."""
    print_section("5. Follow Operations")

    # Follow operations (commented out for safety)
    # print(f"\n👥 Testing follow operations for user: {SAMPLE_USER_ID}")
    # if safe_api_call(cl.follow_user, user_name=SAMPLE_USER_ID):
    #     print("   ✅ User followed successfully")
    # if safe_api_call(cl.unfollow_user, user_name=SAMPLE_USER_ID):
    #     print("   ✅ User unfollowed successfully")

    print("\n⚠️  Follow operations are commented out for safety.")
    print("    Uncomment lines in demo_follow_operations() to test.")


def demo_goal_timeline_operations(cl: StudyPlus) -> None:
    """Demonstrate goal and achievement timeline operations."""
    print_section("6. Goal & Achievement Timeline Operations")

    # Get goal timeline
    print(f"\n🎯 Getting goal timeline for: {SAMPLE_GOAL}")
    goal_tl = safe_api_call(cl.get_goal_timeline, target_id=SAMPLE_GOAL)
    if goal_tl and goal_tl.get('feeds'):
        print(f"✅ Retrieved {len(goal_tl['feeds'])} posts from goal timeline")

        # Like goal post (commented out for safety)
        # if len(goal_tl['feeds']) > 0:
        #     event_id = goal_tl['feeds'][0]['body_study_record']['event_id']
        #     if safe_api_call(cl.like_post, event_id):
        #         print(f"   ✅ Liked goal post {event_id}")

    # Get achievement timeline
    print(f"\n🏆 Getting achievement timeline for: {SAMPLE_GOAL}")
    achievement_tl = safe_api_call(cl.get_achievement_timeline, target_id=SAMPLE_GOAL)
    if achievement_tl and achievement_tl.get('feeds'):
        print(f"✅ Retrieved {len(achievement_tl['feeds'])} posts from achievement timeline")

        # Like achievement post (commented out for safety)
        # if len(achievement_tl['feeds']) > 0:
        #     event_id = achievement_tl['feeds'][0]['body_study_achievement']['event_id']
        #     if safe_api_call(cl.like_post, event_id):
        #         print(f"   ✅ Liked achievement post {event_id}")


def demo_profile_operations(cl: StudyPlus) -> None:
    """Demonstrate profile picture operations."""
    print_section("7. Profile Picture Operations")

    # Download profile picture
    print(f"\n🖼️  Downloading profile picture for: {SAMPLE_USER_ID}")
    result = safe_api_call(
        cl.download_profile_picture,
        user_name=SAMPLE_USER_ID,
        output_file_name=OUTPUT_IMAGE_FILE
    )
    if result:
        print(f"✅ Profile picture saved to {OUTPUT_IMAGE_FILE}")

    # Update profile picture (commented out for safety)
    # print(f"\n🖼️  Updating your profile picture...")
    # if safe_api_call(cl.update_profile_picture, file_path=OUTPUT_IMAGE_FILE):
    #     print("   ✅ Profile picture updated successfully")
    # else:
    #     print("   ⚠️  Profile picture update is commented out for safety.")

    print("\n⚠️  Profile picture update is commented out for safety.")
    print("    Uncomment lines in demo_profile_operations() to test.")


# ==============================================================================
# Main Function
# ==============================================================================

def main():
    """Main function to run the example demonstrations."""
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                        Stplpy Example Script                             ║
║                                                                          ║
║  This script demonstrates various features of the Stplpy library.       ║
║  Potentially dangerous operations are commented out for safety.         ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)

    # Load environment variables
    load_dotenv(".env")

    # Initialize StudyPlus client
    try:
        token = os.environ.get("TOKEN")
        if not token:
            print("❌ ERROR: TOKEN not found in environment variables.")
            print("   Please create a .env file with your TOKEN.")
            return

        cl = StudyPlus(token)
        print("✅ StudyPlus client initialized successfully\n")
    except Exception as e:
        print(f"❌ Failed to initialize StudyPlus client: {e}")
        return

    # Run demonstrations
    try:
        # Get user info first (needed for some demos)
        myself = safe_api_call(cl.get_myself)

        # Run all demo functions
        demo_user_information(cl)
        demo_timeline_operations(cl)
        demo_post_operations(cl)
        demo_study_record_operations(cl, myself)
        demo_follow_operations(cl)
        demo_goal_timeline_operations(cl)
        demo_profile_operations(cl)

        # Completion message
        print_section("Demo Complete")
        print("""
✅ All demonstrations completed successfully!

📝 Note: Operations that modify data (follow, post, delete, etc.) are
   commented out for safety. Review and uncomment them carefully if you
   want to test those features.

📁 Output files:
   - {}: Post details in JSON format
   - {}: Downloaded profile picture

💡 Tip: You can customize the sample IDs at the top of this script.
        """.format(OUTPUT_JSON_FILE, OUTPUT_IMAGE_FILE))

    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Unexpected error during demo: {e}")


if __name__ == "__main__":
    main()
