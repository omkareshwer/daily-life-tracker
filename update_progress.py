import json
from datetime import datetime, timedelta

USER_NAME = "Parthsinh"

def get_rank_details(xp):
    if xp < 500:
        return "Novice Tracker", "ff4757"  # Red
    elif xp < 1500:
        return "Habit Apprentice", "eccc68"  # Gold
    elif xp < 3500:
        return "Consistency Master", "2ed573"  # Emerald Green
    else:
        return "Legendary Life-Hacker", "70a1ff"  # Blue

def calculate_streak(history_dates):
    if not history_dates:
        return 0
    
    sorted_dates = sorted(list(set(history_dates)), reverse=True)
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    date_objs = [datetime.strptime(d, '%Y-%m-%d').date() for d in sorted_dates]
    
    if today not in date_objs and yesterday not in date_objs:
        return 0
        
    streak = 0
    check_date = today if today in date_objs else yesterday
    
    while check_date in date_objs:
        streak += 1
        check_date -= timedelta(days=1)
        
    return streak

def run():
    today_dt = datetime.now()
    today_str = today_dt.strftime('%Y-%m-%d')

    with open('tasks.json', 'r') as f:
        data = json.load(f)

    # Calculate XP added today
    today_xp = sum(t['xp'] for t in data['daily_tasks'] if t.get('completed'))
    data['total_xp'] += today_xp

    all_completed_dates = []

    # Update task history and reset completion status
    for t in data['daily_tasks']:
        if 'history' not in t:
            t['history'] = []
            
        if t.get('completed'):
            if today_str not in t['history']:
                t['history'].append(today_str)
            t['completed'] = False
            
        all_completed_dates.extend(t['history'])

    # Save updated JSON back
    with open('tasks.json', 'w') as f:
        json.dump(data, f, indent=2)

    total_xp = data['total_xp']
    rank_name, badge_color = get_rank_details(total_xp)
    current_streak = calculate_streak(all_completed_dates)

    # Level calculation for progress bar
    levels = [500, 1500, 3500, 10000]
    target_xp = min([l for l in levels if l > total_xp], default=10000)
    prev_target = 0
    for l in levels:
        if total_xp >= l:
            prev_target = l
        else:
            break
            
    current_level_xp = total_xp - prev_target
    needed_xp = max(target_xp - prev_target, 1)
    percentage = min(int((current_level_xp / needed_xp) * 100), 100)

    # URL Encoded Safe Badges (No raw emoji inside badge URLs)
    clean_rank = rank_name.replace(' ', '_')
    streak_badge = f"https://img.shields.io/badge/Streak-{current_streak}_Days-ff6b81?style=for-the-badge&logo=gitbook&logoColor=white"
    xp_badge = f"https://img.shields.io/badge/Total_XP-{total_xp}_XP-70a1ff?style=for-the-badge&logo=gamepad&logoColor=white"
    rank_badge = f"https://img.shields.io/badge/Rank-{clean_rank}-{badge_color}?style=for-the-badge&logo=shield&logoColor=white"

    lines = []
    
    # 1. Header Banner
    lines.append(f"![Header Banner](https://capsule-render.vercel.app/api?type=rect&color=0:09090e,100:1a1a2e&height=180&section=header&text=🎮%20{USER_NAME}'S%20HABIT%20TRACKER&fontSize=34&fontColor=00f0ff&animation=fadeIn)\n")
    
    # 2. Clean Badges Line
    lines.append(f"![Rank]({rank_badge}) ![Streak]({streak_badge}) ![XP]({xp_badge})\n")
    
    # 3. Progress Card
    lines.append("> [!IMPORTANT]")
    lines.append(f"> ### 🚀 **Level Progress: {percentage}%**")
    lines.append(f"> <progress value=\"{percentage}\" max=\"100\" style=\"width:100%; height:18px;\"></progress>")
    lines.append(f"> 🎯 **Current:** `{current_level_xp} XP` | 🏁 **Target:** `{target_xp} XP` (Need `{needed_xp - current_level_xp} XP` more)\n")

    lines.append("\n---\n")
    lines.append("## 🏆 Reward Matrix & Status\n")
    lines.append("| Level | Required XP | Reward | Status |")
    lines.append("| :---: | :---: | :--- | :---: |")

    for r in data['rewards']:
        status = "🟢 **UNLOCKED**" if total_xp >= r['required_xp'] else "🔴 **LOCKED**"
        lines.append(f"| **{r['level']}** | `{r['required_xp']} XP` | {r['reward']} | {status} |")

    lines.append("\n---\n")
    lines.append("## 📋 Daily Tasks Dashboard\n")
    lines.append("| Task Title | XP Reward | Total Completed | Last Activity |")
    lines.append("| :--- | :---: | :---: | :---: |")

    for t in data['daily_tasks']:
        completed_count = len(t.get('history', []))
        last_date = t['history'][-1] if t.get('history') else "Never"
        lines.append(f"| ⚡ {t['title']} | `+{t['xp']} XP` | `{completed_count} times` | `{last_date}` |")

    lines.append("\n---\n")
    lines.append("## 📅 7-Day Performance Log\n")
    lines.append("| Day | Date | Status |")
    lines.append("| :---: | :---: | :---: |")

    for i in range(6, -1, -1):
        day_date = (today_dt - timedelta(days=i)).strftime('%Y-%m-%d')
        day_name = (today_dt - timedelta(days=i)).strftime('%a')
        was_active = any(day_date in t.get('history', []) for t in data['daily_tasks'])
        status_icon = "🔥 **ACTIVE**" if was_active else "⚪ *MISSED*"
        lines.append(f"| {day_name} | `{day_date}` | {status_icon} |")

    lines.append(f"\n> [!TIP]\n> Keep grinding daily, **{USER_NAME}**! Complete tasks in `tasks.json` to keep your streak alive! ⚡")

    readme_content = "\n".join(lines)

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

if __name__ == '__main__':
    run()
