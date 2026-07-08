from ai.brain import ask_ai
from core.scheduler import Scheduler
from core.decision_engine import DecisionEngine


scheduler = Scheduler()
decision_engine = DecisionEngine()


def process_message(message, history):
    if not decision_engine.should_use_ai(message):
        return "I don't need to respond."

    if not scheduler.can_think():
        return "..."

    return ask_ai(message, history)