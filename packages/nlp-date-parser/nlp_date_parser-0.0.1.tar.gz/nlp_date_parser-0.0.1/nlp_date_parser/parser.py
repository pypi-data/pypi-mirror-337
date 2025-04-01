from datetime import datetime, timedelta
import re
from dateutil import parser, relativedelta

class NLPDateParser:
    def __init__(self):
        self.relative_patterns = [
            (r'(?i)next (monday|tuesday|wednesday|thursday|friday|saturday|sunday)', self._parse_next_weekday),
            (r'(?i)last (monday|tuesday|wednesday|thursday|friday|saturday|sunday)', self._parse_last_weekday),
            (r'(?i)in (\d+) (seconds|minutes|hours|days|weeks|months|years)', self._parse_relative_time),
            (r'(?i)(tomorrow|today|yesterday)', self._parse_simple_day)
        ]

    def parse(self, text: str) -> datetime:
        text = text.strip()
        
        # Try direct date parsing
        try:
            return parser.parse(text)
        except ValueError:
            pass
        
        # Try relative patterns
        for pattern, handler in self.relative_patterns:
            match = re.search(pattern, text)
            if match:
                return handler(match)
        
        raise ValueError(f"Could not parse date from: {text}")

    def _parse_next_weekday(self, match):
        weekday = match.group(1).lower()
        today = datetime.today()
        target_weekday = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'].index(weekday)
        days_ahead = (target_weekday - today.weekday() + 7) % 7
        return today + timedelta(days=days_ahead if days_ahead else 7)

    def _parse_last_weekday(self, match):
        weekday = match.group(1).lower()
        today = datetime.today()
        target_weekday = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'].index(weekday)
        days_behind = (today.weekday() - target_weekday + 7) % 7
        return today - timedelta(days=days_behind if days_behind else 7)

    def _parse_relative_time(self, match):
        value, unit = int(match.group(1)), match.group(2).lower()
        delta_map = {
            "seconds": timedelta(seconds=value),
            "minutes": timedelta(minutes=value),
            "hours": timedelta(hours=value),
            "days": timedelta(days=value),
            "weeks": timedelta(weeks=value),
            "months": relativedelta.relativedelta(months=value),
            "years": relativedelta.relativedelta(years=value)
        }
        return datetime.now() + delta_map[unit]

    def _parse_simple_day(self, match):
        today = datetime.today()
        day_map = {
            "today": today,
            "tomorrow": today + timedelta(days=1),
            "yesterday": today - timedelta(days=1)
        }
        return day_map[match.group(1).lower()]
 
