from typing import Any, Text, Dict, List

import arrow
import dateparser
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

city_db = {
    'colombo': 'Asia/Calcutta',
    'srilanka': 'Asia/Calcutta',
    'sri lanka': 'Asia/Calcutta',
    'india': 'Asia/Calcutta',
    'kandy': 'Asia/Calcutta',
    'london': 'Europe/Dublin',
    'brussels': 'Europe/Zagreb',
    'lisbon': 'Europe/Lisbon',
    'amsterdam': 'Europe/Amsterdam',
    'seattle': 'US/Pacific'
}


class ActionTellTime(Action):

    def name(self) -> Text:
        return "action_telltime"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_place = next(tracker.get_latest_entity_values("place"), None)
        utc = arrow.utcnow()
        ind_time = arrow.now('Asia/Calcutta')

        if not current_place:
            msg = f"It's {utc.format('HH:mm')} utc and {ind_time.format('HH:mm')} ist now. You can also give me a place"
            dispatcher.utter_message(text=msg)
            return []

        tz_string = city_db.get(current_place, None)
        if not tz_string:
            msg = f"It's I didn't recognize {current_place}. Is it spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []

        msg = f"It's {utc.to(city_db[current_place]).format('HH:mm')} in {current_place} now."
        dispatcher.utter_message(text=msg)

        return []
