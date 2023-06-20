import datetime
import time

class TimeKeeper:
    upcoming_actions = {}

    def __init__(self, username, action, sleep_time_in_seconds):
        self.username = username
        self.action = action
        self.sleep_time_in_seconds = sleep_time_in_seconds
        self.next_action_time = datetime.datetime.now() + datetime.timedelta(seconds=sleep_time_in_seconds)
        self.next_action_time_formatted = self.next_action_time.strftime("%B %d, %Y, %I:%M %p")
        print(f"Next execution time for {username}'s action {action}: {self.next_action_time_formatted}")

        # If the user does not already exist in the upcoming actions, create a new list for them
        if username not in TimeKeeper.upcoming_actions:
            TimeKeeper.upcoming_actions[username] = []

        # Append the action and its execution time to the user's list of upcoming actions
        TimeKeeper.upcoming_actions[username].append((action, self.next_action_time))

    @staticmethod
    def get_upcoming_actions(username):
        if username in TimeKeeper.upcoming_actions:
            return [(action, time.strftime("%B %d, %Y, %I:%M %p")) for action, time in TimeKeeper.upcoming_actions[username]]
        else:
            return []
