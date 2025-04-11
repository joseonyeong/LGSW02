read -p "커밋 메시지 입력: " user_message

current_time=$(TZ=Asia/Seoul date "+%Y-%m-%d %H:%M:%S")

commit_message="$user_message | $current_time (KST)"

git add .
git commit -m "$(date '+%Y-%m-%d %H:%M:%S')"
git push

