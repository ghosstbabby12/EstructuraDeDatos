from datetime import datetime, timedelta
import pytz
import json
import os

# -----------------------------
# TIMEZONE UTILITIES
# -----------------------------

def save_alarms_to_file(alarms, filename="alarms.json"):
    with open(filename, "w") as f:
        json.dump(alarms, f)

def load_alarms_from_file(filename="alarms.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

def get_country_timezones(country_code="PE"):
    """
    Returns all timezones for a given country code (e.g., "PE" for Peru).
    """
    try:
        return pytz.country_timezones[country_code]
    except KeyError:
        return []

def get_timezones():
    """
    Returns a sorted list of all available timezones.
    """
    return sorted(pytz.all_timezones)

def get_current_time_in_timezone(timezone_str):
    """
    Returns the current datetime object in the specified timezone.
    """
    timezone = pytz.timezone(timezone_str)
    return datetime.now(timezone)

def format_time(dt):
    """
    Formats a datetime object into a string: "YYYY-MM-DD HH:MM:SS".
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# -----------------------------
# ALARM UTILITIES
# -----------------------------

def check_alarm(current_time_str, alarm_time_str):
    """
    Compares the current time string (HH:MM) with the alarm time string.
    Returns True if they match.
    """
    return current_time_str[:5] == alarm_time_str

# -----------------------------
# TIMER UTILITIES
# -----------------------------

class Timer:
    def __init__(self, minutes=0, seconds=0):
        self.initial_duration = timedelta(minutes=minutes, seconds=seconds)
        self.remaining = self.initial_duration
        self.running = False
        self.start_time = None

    def start(self):
        if not self.running:
            self.running = True
            self.start_time = datetime.now()

    def pause(self):
        if self.running:
            elapsed = datetime.now() - self.start_time
            self.remaining -= elapsed
            self.running = False

    def reset(self):
        self.remaining = self.initial_duration
        self.running = False
        self.start_time = None

    def get_time_left(self):
        if self.running:
            elapsed = datetime.now() - self.start_time
            remaining = self.remaining - elapsed
        else:
            remaining = self.remaining

        if remaining.total_seconds() < 0:
            return "00:00"
        mins, secs = divmod(int(remaining.total_seconds()), 60)
        return f"{mins:02d}:{secs:02d}"
