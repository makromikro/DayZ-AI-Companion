class DecisionEngine:

    def should_use_ai(self, message):

        if not message:
            return False

        message = message.strip()

        if len(message) == 0:
            return False

        return True