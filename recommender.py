import random


class BurnoutRecommender:
    def __init__(self):
        # 📚 Knowledge Base: The "Items" we can recommend
        # Categories: Sleep, Social, Study, Health
        self.intervention_database = {
            'sleep_deprivation': [
                "🌙 **Digital Sunset:** Turn off all screens 1 hour before bed to lower cortisol.",
                "🧘 **NSDR Protocol:** Try a 10-minute Non-Sleep Deep Rest session (search on YouTube).",
                "☕ **Caffeine Cutoff:** No coffee after 2:00 PM today.",
                "🌡️ **Thermoregulation:** Lower your room temperature to 18°C for better deep sleep."
            ],
            'isolation': [
                "📞 **Micro-Socializing:** Call a friend or family member for just 5 minutes.",
                "🚶 **Public Walk:** Go study in a library or coffee shop to be around people.",
                "🤝 **Study Buddy:** Find a partner to review today's material with.",
                "💬 **Text Check-in:** Send a message to 3 friends you haven't seen in a while."
            ],
            'overwork': [
                "🍅 **Pomodoro Reset:** Switch to 25m work / 5m break immediately.",
                "🛑 **Hard Stop:** Set a rigid alarm to stop studying at 9:00 PM.",
                "📉 **The 80/20 Rule:** Identify the 20% of tasks that give 80% of results and drop the rest.",
                "🌳 **Nature Break:** Step outside for 15 minutes without your phone."
            ],
            'sedentary': [
                "🤸 **Desk Stretch:** Do a 2-minute spinal twist and neck stretch right now.",
                "🚶 **Walking Meeting:** Listen to your lecture recording while walking.",
                "🥤 **Hydration Game:** Drink a full glass of water for every hour of study.",
                "👀 **20-20-20 Rule:** Every 20 mins, look 20 feet away for 20 seconds."
            ]
        }

    def get_recommendations(self, daily_stats, is_anomaly):
        recommendations = []
        triggers = []

        # 1. Analyze specific triggers (Rule-based filtering)
        if daily_stats.get('sleep_hours', 8) < 6.0:
            triggers.append('sleep_deprivation')

        if daily_stats.get('social_hours', 2) < 0.5:
            triggers.append('isolation')

        if daily_stats.get('study_hours', 4) > 9.0:
            triggers.append('overwork')

        if daily_stats.get('exercise_minutes', 30) < 15:
            triggers.append('sedentary')

        # 2. Select Advice
        if not triggers and not is_anomaly:
            # User is doing well
            return [" **Maintenance:** Your habits are balanced. Keep maintaining this routine!"]

        # If Anomaly is detected but no obvious trigger, assume general stress
        if is_anomaly and not triggers:
            triggers.append('overwork')  # Default to overwork advice for anomalies

        # Fetch random tips for each active trigger
        for trigger in triggers:
            # Get specific advice for this problem
            tips = self.intervention_database[trigger]
            # Pick one random tip to keep it fresh
            advice = random.choice(tips)
            recommendations.append(advice)

        return recommendations


# --- Testing Block ---
if __name__ == "__main__":
    rec = BurnoutRecommender()

    # Test Case: A "Burnout" student
    test_stats = {
        'sleep_hours': 4.0,
        'study_hours': 10.0,
        'social_hours': 0.0,
        'exercise_minutes': 0
    }

    print("User Stats:", test_stats)
    print("Recommendations:")
    for r in rec.get_recommendations(test_stats, is_anomaly=True):
        print(r)