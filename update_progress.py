import json
from datetime import datetime, timedelta

def get_rank_and_badge(xp):
    if xp < 500:
        return "🥉 Novice Tracker"
    elif xp < 1500:
        return "🥈 Habit Apprentice"
    elif xp < 3500:
        return "🥇 Consistency Master"
    else:
        return "👑 Legendary Life-Hacker"

def generate_progress_bar(xp, next_target=500):
    # Target levels
    levels = [500, 1500, 3500, 10000]
    target = min([l for l in levels if l > xp], default=10000)
    
    prev_target = 0
    for l in levels:
        if xp >= l:
            prev_target = l
        else:
            break
            
    current_level_xp = xp - prev_target
    needed_xp = target - prev_target
    
    percentage = min(int((current_level_xp / needed_xp) * 100), 100)
    filled_length = int(percentage // 10)
    bar = "█" * filled_length + "░" * (10 - filled_length)
    
    return f"[{bar}] {percentage}% ({xp}/{target} XP)", target

def calculate_streak(history_dates):
    if not history_dates:
        return 0
    
    sorted_dates = sorted(list(set(history_dates)), reverse=True)
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    # Dates conversion
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

    # Collect all dates for streak
    all_completed_dates = []

    # Update task history and reset completion
    for t in data['daily_tasks']:
        if 'history' not in t:
            t['history'] = []
            
        if t.get('completed'):
            if today_str not in t['history']:
                t['history'].append(today_str)
            t['completed'] = False
            
        all_completed_dates.extend(t['history'])

    # Save back to tasks.json
    with open('tasks.json', 'w') as f:
        json.dump(data, f, indent=2)

    total_xp = data['total_xp']
    rank = get_rank_and_badge(total_xp)
    progress_bar, next_target = generate_progress_bar(total_xp)
    current_streak = calculate_streak(all_completed_dates)

    # Build README Markdown
    readme_content = f"""# 🎮 Daily Life & Habit Tracker

<div align="center">

### 🛡️ **Current Rank:** `{rank}`
### 🔥 **Streak:** `{current_streak} Days` | 📊 **Total XP:** `{total_xp} XP`

```text
Level Progress: {progress_bar}
