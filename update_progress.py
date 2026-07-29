
import json

def run():
    with open('tasks.json', 'r') as f:
        data = json.load(f)

    # Today's XP calculation
    today_xp = sum(t['xp'] for t in data['daily_tasks'] if t['completed'])
    data['total_xp'] += today_xp

    # Reset tasks completed status for next day
    for t in data['daily_tasks']:
        t['completed'] = False

    # Save updated total_xp
    with open('tasks.json', 'w') as f:
        json.dump(data, f, indent=2)

    total_xp = data['total_xp']

    # Build README content
    readme_content = f"""# 🎮 Daily Life & Habit Tracker

### 📊 Current Score Board
- **Total XP Earned:** `{total_xp} XP`
- **Last Updated:** Today

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

## 📋 Standard Tasks List

| Task Title | XP Value |
| :--- | :--- |
"""
    for t in data['daily_tasks']:
        readme_content += f"| {t['title']} | +{t['xp']} XP |\n"

    readme_content += "\n> *Update `tasks.json` daily and commit to gain XP and unlock rewards!*"

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

if __name__ == '__main__':
    run()
