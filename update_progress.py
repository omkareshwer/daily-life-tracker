import json
from datetime import datetime

def run():
    # Aaj ki date (YYYY-MM-DD format me)
    today_str = datetime.now().strftime('%Y-%m-%d')

    with open('tasks.json', 'r') as f:
        data = json.load(f)

    # Today's XP calculation
    today_xp = sum(t['xp'] for t in data['daily_tasks'] if t.get('completed'))
    data['total_xp'] += today_xp

    # Date logging aur reset logic
    for t in data['daily_tasks']:
        # Agar history list nahi hai toh create kar do
        if 'history' not in t:
            t['history'] = []
        
        # Agar aaj complete hua hai aur pehle se date added nahi hai
        if t.get('completed'):
            if today_str not in t['history']:
                t['history'].append(today_str)
            t['completed'] = False  # Next day ke liye reset

    # Save updated JSON
    with open('tasks.json', 'w') as f:
        json.dump(data, f, indent=2)

    total_xp = data['total_xp']

    # Build README content
    readme_content = f"""# 🎮 Daily Life & Habit Tracker

### 📊 Current Score Board
- **Total XP Earned:** `{total_xp} XP`
- **Last Updated:** `{today_str}`

---

## 🏆 Reward Matrix & Status

| Level | Required XP | Reward | Status |
| :--- | :--- | :--- | :--- |
"""

    for r in data['rewards']:
        status = "✅ UNLOCKED" if total_xp >= r['required_xp'] else "🔒 Locked"
        readme_content += f"| {r['level']} | {r['required_xp']} XP | {r['reward']} | **{status}** |\n"

    readme_content += """
---

## 📋 Standard Tasks & Activity Log

| Task Title | XP Value | Total Times Completed | Last Completed Date |
| :--- | :--- | :--- | :--- |
"""
    for t in data['daily_tasks']:
        completed_count = len(t.get('history', []))
        last_date = t['history'][-1] if t.get('history') else "Never"
        readme_content += f"| {t['title']} | +{t['xp']} XP | {completed_count} times | `{last_date}` |\n"

    readme_content += "\n> *Update `tasks.json` daily and commit to gain XP and unlock rewards!*"

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

if __name__ == '__main__':
    run()
