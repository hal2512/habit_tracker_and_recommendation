import random
import pyttsx3
import threading
from recommender import BurnoutRecommender


class GuardianChatbot:
    def __init__(self):
        self.recommender = BurnoutRecommender()
        self.name = "The Guardian"

        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)
        except:
            self.engine = None
            print("⚠️ Warning: TTS Engine could not start. Voice disabled.")

        self.intents = {
            # --- BASICS ---
            'greeting': {
                'patterns': ['hi', 'hello', 'hey', 'start', 'wake up', 'good morning', 'good evening'],
                'responses': [
                    "Hello. I am The Guardian. I am here to protect your wellness balance.",
                    "Hi there. I'm monitoring your habits to keep you safe from burnout.",
                    "Greetings. How are you feeling today?"
                ]
            },
            'goodbye': {
                'patterns': ['bye', 'goodbye', 'see you', 'exit', 'quit', 'stop'],
                'responses': [
                    "Stay balanced. Goodbye.",
                    "Rest well. I will continue monitoring your patterns.",
                    "Goodbye. Don't forget to log your stats tomorrow."
                ]
            },

            # --- EMOTIONAL SUPPORT ---
            'sad/tired': {
                'patterns': ['tired', 'exhausted', 'sad', 'stressed', 'burnout', 'bad', 'anxious', 'depressed',
                             'overwhelmed'],
                'responses': [
                    "I hear you. High stress is often a signal to pause. Have you checked your sleep stats today?",
                    "It's okay to not be okay. My data suggests you might be pushing too hard.",
                    "I'm sorry you're feeling this way. Remember that rest is productive too."
                ]
            },
            'motivation': {
                'patterns': ['motivate', 'inspiration', 'hard', 'give up', 'can\'t do this', 'encourage'],
                'responses': [
                    "You don't need to be perfect, you just need to be consistent.",
                    "Burnout happens when you avoid rest. Take a break, then come back stronger.",
                    "One step at a time. Check your dashboard—small improvements add up."
                ]
            },

            # --- SPECIFIC ADVICE CATEGORIES ---
            'sleep_advice': {
                'patterns': ['cant sleep', 'insomnia', 'awake', 'sleep tip', 'better sleep'],
                'responses': [
                    "Try the 10-3-2-1 rule: No caffeine 10h before bed, no food 3h before, no work 2h before, no screens 1h before.",
                    "Lower your room temperature to 18°C (65°F). It signals your body it's time to rest.",
                    "If you can't sleep after 20 minutes, get up and do something boring in dim light until you are tired."
                ]
            },
            'study_tips': {
                'patterns': ['study tip', 'focus', 'concentration', 'distracted', 'cant study'],
                'responses': [
                    "Try the Pomodoro technique: 25 minutes of focus, 5 minutes of rest. I can help you track this.",
                    "Put your phone in another room. Physical distance reduces cognitive load.",
                    "Try 'Active Recall'. Don't just read; close the book and try to explain the concept out loud."
                ]
            },
            'stress_relief': {
                'patterns': ['calm down', 'panic', 'anxiety', 'relax', 'breathe'],
                'responses': [
                    "Try 'Box Breathing': Inhale for 4s, Hold for 4s, Exhale for 4s, Hold for 4s.",
                    "Look around and name 5 things you can see, 4 you can touch, and 3 you can hear. It grounds you.",
                    "Step away from the screen. Look at something green or natural for 2 minutes."
                ]
            },

            # --- SYSTEM COMMANDS ---
            'status': {
                'patterns': ['status', 'stats', 'how am i doing', 'score', 'report', 'data'],
                'responses': [
                    "Please check the Dashboard page for your real-time Safety Score.",
                    "I am analyzing your data... check the main page for the full report.",
                    "Your latest data point is being processed on the Dashboard."
                ]
            },
            'help': {
                'patterns': ['help', 'what can you do', 'assist', 'features', 'who are you'],
                'responses': [
                    "I detect anomalies in your study and sleep habits. I can recommend recovery protocols if you say 'recommend'.",
                    "I am a Burnout Prevention System. I track your sleep, study, and social patterns to warn you before you crash."
                ]
            }
        }

    def speak(self, text):
        if self.engine:
            def _speak():
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                except:
                    pass

            thread = threading.Thread(target=_speak)
            thread.start()

    def get_response(self, user_input, current_stats=None, is_risk=False):
        user_input = user_input.lower()
        response = ""

        if 'recommend' in user_input or 'advice' in user_input or 'fix' in user_input:
            if current_stats:
                recs = self.recommender.get_recommendations(current_stats, is_risk)
                response = "Here is my protection protocol for you. " + recs[0]
                full_text = "Here is my protection protocol for you:\n\n" + "\n".join(recs)
                self.speak(response)
                return full_text
            else:
                response = "I need to see your daily stats first. Please go to the Dashboard and log your day."
                self.speak(response)
                return response

        intent_found = False
        for intent_name, data in self.intents.items():
            for pattern in data['patterns']:
                if pattern in user_input:
                    response = random.choice(data['responses'])
                    intent_found = True
                    break
            if intent_found: break

        if not response:
            response = "I am listening. Tell me more about your habits, or say 'help' to see what I can do."

        self.speak(response)
        return response