from brain import ask_ai
from scheduler import Scheduler
from decision_engine import DecisionEngine


scheduler = Scheduler()
decision_engine = DecisionEngine()


def process_message(message, history):
    """
    Main runtime entry point.
    Every message passes through here.
    """

    if not decision_engine.should_use_ai(message):
        return "I don't need to respond."

    if not scheduler.can_think():
        return "..."

    return ask_ai(message, history)