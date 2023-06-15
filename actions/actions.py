from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


puzzle_prompts = {
    "date_puzzle" : "I was only 25 years old the day before yesterday and next year I'll be 28. What is the only date this can happen?",
    "worldcup_puzzle": "What is the Nation with the most Football World Cups?",
    "wet_puzzle": "What gets wet when drying?",
    "fourth_puzzle": "There are no riddles to be solved",
}

puzzle_hints = {
    "date_puzzle" : ["It is a date between December and January", "It is closer to the end of the year", "First of....", "Even my dog would have solved this already...", "The answer is: First of January, but common bro..."],
    "worldcup_puzzle": ["It is the largest country in South America", "They speak portuguese in this country", "Bra...", "Even my dog would have solved this already...", "The answer is: Brazil, but common bro..."],
    "wet_puzzle": ["You can find this item in your bathroom", "You use it (hopefully) everyday when you take a shower", "To...", "Even my dog would have solved this already...", "The answer is: Towel, but common bro..."],
    "fourth_puzzle": ["There are no hints since there are no puzzles to be solved"],
}

# class ActionSessionStarted(Action):
#     def name(self) -> Text:
#         return "action_session_started"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         if tracker.get_slot("current_puzzle_to_solve") is None:
#             dispatcher.utter_message(text="Subject 69, please say your name out loud as you type it in...")
#             #We initialize the total amount of lives for the player, in this case 10
#             return[SlotSet("lives", 10)]
#         dispatcher.utter_message(text="Sorry I do not understand. Can you rephrase it?")
#         return[]

class ActionSayName(Action):

    def name(self) -> Text:
        return "action_say_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        if not name:
            dispatcher.utter_message(text="I don't know your name.")
            return[]
        else:
            if tracker.get_slot("current_puzzle_to_solve") is None:
                dispatcher.utter_message(text=f"Hi {name}...")
                dispatcher.utter_message(text="Suddenly the lights went out. All you see is a door with phosphorescent neon lights in front of you that says 'I was only 25 years old the day before yesterday and next year I'll be 28. What is the only date this can happen?'.")
                dispatcher.utter_message(text="As you approach you find the door lock with some inscriptions: 'Can you guess me?'....")
                return [SlotSet("name", name), SlotSet("current_puzzle_to_solve", "date_puzzle"), SlotSet("lives", 10)]
            else:
                dispatcher.utter_message(text=f"Sorry I don't understand. Can you rephrase it?")
                return []
            

class ActionRiddleCheck(Action):

    def __init__(self):
        self.possible_corret_answers = ["first of january", "1st january", "01.01", "1 january", "january 1", "january first"]
        self.already_solved = False
        self.puzzle_name = "date_puzzle"

    def name(self) -> Text:
        return "action_say_is_date_riddle_correct"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_puzzle_to_be_solved = tracker.get_slot("current_puzzle_to_solve")

        if current_puzzle_to_be_solved:
            if current_puzzle_to_be_solved != self.puzzle_name:
                dispatcher.utter_message(text=f"Sorry I don't understand. Can you rephrase it?")
                return []

        answer_date = tracker.get_slot("answer_date")
        if not answer_date:
            dispatcher.utter_message(text="Repeat your answer please.")
            return []

        else:
            for answer in self.possible_corret_answers: 
                if answer_date.lower() == answer:
                    dispatcher.utter_message(text=f"The lock fell off and you try to open the door. Unfortunately the door is still locked.")
                    dispatcher.utter_message(text=f"You see another lock with more inscriptions: What is the Nation with the most Football World Cups?")
                    self.already_solved = True

                    puzzles_solved_num = tracker.get_slot("number_puzzle_solved")
                    if puzzles_solved_num is None:
                        puzzles_solved_num = 1
                    else:
                        puzzles_solved_num += 1

                    #We have to update we entered to a new room and that we have solved a puzzle
                    return [SlotSet("number_puzzle_solved", puzzles_solved_num), SlotSet("current_puzzle_to_solve", "worldcup_puzzle")]


            

            current_lives = tracker.get_slot("lives")
            if current_lives < 2:
                dispatcher.utter_message(text=f"GAME OVER.")
                return []

            dispatcher.utter_message(text=f"The door is still locked...Try again")
            dispatcher.utter_message(text=f"You have lost a life! You have {current_lives-1} lives left.")


            return [SlotSet("lives", current_lives-1)]



class GetCurrentRoomAction(Action):

    def name(self) -> Text:
        return "action_get_current_room"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_room = tracker.get_slot("current_room")
        # print(current_room)
        if not current_room:
            dispatcher.utter_message(text="You are in the starting room")
        else:
            dispatcher.utter_message(text=f"You are in the {current_room}!")
        return []

class GetNumberPuzzlesSolvedAction(Action):

    def name(self) -> Text:
        return "action_get_number_puzzle_solved"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        number_puzzle_solved = tracker.get_slot("number_puzzle_solved")
        if not number_puzzle_solved:
            dispatcher.utter_message(text=f"No puzzles solved.")
        else:
            dispatcher.utter_message(text=f"You have solved {number_puzzle_solved} puzzles!")
        return []

class GetCurrentPuzzlePromptAction(Action):

    def name(self) -> Text:
        return "action_get_current_puzzle_prompt"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_puzzle= tracker.get_slot("current_puzzle_to_solve")
        if not current_puzzle:
            dispatcher.utter_message(text=f"No puzzles to be solved.")
        else:
            dispatcher.utter_message(text=f"{puzzle_prompts[current_puzzle]}")
        return []

class DefaultFallbackAction(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Custom fallback response message
        fallback_message = "I'm sorry, I didn't understand. Can you please rephrase your message?"

        # Send the fallback message
        dispatcher.utter_message(text=fallback_message)

        return []


class WorldCupRiddleCheck(Action):
    def __init__(self):
        self.puzzle_name = "worldcup_puzzle"

    def name(self) -> Text:
        return "action_say_is_world_cup_riddle_correct"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_puzzle_to_be_solved = tracker.get_slot("current_puzzle_to_solve")

        if current_puzzle_to_be_solved:
            if current_puzzle_to_be_solved != self.puzzle_name:
                dispatcher.utter_message(text=f"Sorry I don't understand. Can you rephrase it?")
                return []


        world_cup_answer = tracker.get_slot("answer_world_cup")

        if world_cup_answer:
            if world_cup_answer.lower() == "brazil":
                dispatcher.utter_message(text=f"The second lock fell off and you try to open the door. Unfortunately the door is still locked.")
                dispatcher.utter_message(text=f"You see another lock with more inscriptions: What gets wet when drying?")

                puzzles_solved_num = tracker.get_slot("number_puzzle_solved")
                if puzzles_solved_num is None:
                    puzzles_solved_num = 1
                else:
                    puzzles_solved_num += 1
                return [SlotSet("number_puzzle_solved", puzzles_solved_num), SlotSet("current_puzzle_to_solve", "wet_puzzle")]

            else:
                
                current_lives = tracker.get_slot("lives")
                if current_lives < 2:
                    dispatcher.utter_message(text=f"GAME OVER.")
                    return []

                dispatcher.utter_message(text=f"Wrong! Try again looser")
                dispatcher.utter_message(text=f"You have lost a life! You have {current_lives-1} lives left.")


                return [SlotSet("lives", current_lives-1)]

        dispatcher.utter_message(text=f"I do not understand")

        return []

class WetRiddleCheck(Action):
    def __init__(self):
        self.puzzle_name = "wet_puzzle"

    def name(self) -> Text:
        return "action_say_is_wet_riddle_correct"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_puzzle_to_be_solved = tracker.get_slot("current_puzzle_to_solve")

        if current_puzzle_to_be_solved:
            if current_puzzle_to_be_solved != self.puzzle_name:
                dispatcher.utter_message(text=f"Sorry I don't understand. Can you rephrase it?")
                return []


        wet_answer = tracker.get_slot("answer_wet")

        if wet_answer:
            if wet_answer.lower() == "towel" or wet_answer.lower() == "towels":

                puzzles_solved_num = tracker.get_slot("number_puzzle_solved")
                if puzzles_solved_num is None:
                    puzzles_solved_num = 1
                else:
                    puzzles_solved_num += 1
                
                if puzzles_solved_num == 3:
                    dispatcher.utter_message(text=f"The third lock has fallen off. You try again to open the door and it opens without much effort.")
                    dispatcher.utter_message(text=f"Congrats! You made your way out!")
                    return [SlotSet("number_puzzle_solved", puzzles_solved_num), SlotSet("current_room", "Lobby"), SlotSet("current_puzzle_to_solve", "fourth_puzzle")]

                return [SlotSet("number_puzzle_solved", puzzles_solved_num), SlotSet("current_puzzle_to_solve", "fourth_puzzle")]

            else:
                
                current_lives = tracker.get_slot("lives")
                if current_lives < 2:
                    dispatcher.utter_message(text=f"GAME OVER.")
                    return []
                dispatcher.utter_message(text=f"Wrong! Try again looser")
                dispatcher.utter_message(text=f"You have lost a life! You have {current_lives-1} lives left.")


                return [SlotSet("lives", current_lives-1)]

        dispatcher.utter_message(text=f"I do not understand")

        return []

class GetHints(Action):
    def name(self) -> Text:
        return "action_get_hints"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot("current_puzzle_to_solve") is None:
            dispatcher.utter_message(text="There are no puzzles yet! Please enter your name first!")
            return[]

        current_puzzle = tracker.get_slot("current_puzzle_to_solve")
        

        if current_puzzle == "date_puzzle":
            current_hint_attempt = tracker.get_slot("date_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0

            if current_hint_attempt > 2:
                current_hint_attempt = 2

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("date_puzzle_hint_count", current_hint_attempt + 1)]

        elif current_puzzle == "worldcup_puzzle":
            current_hint_attempt = tracker.get_slot("worldcup_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0

            if current_hint_attempt > 2:
                current_hint_attempt = 2

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("worldcup_puzzle_hint_count", current_hint_attempt + 1)]

        elif current_puzzle == "wet_puzzle":
            current_hint_attempt = tracker.get_slot("wet_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0
                
            if current_hint_attempt > 2:
                current_hint_attempt = 2

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("wet_puzzle_hint_count", current_hint_attempt + 1)]

        elif current_puzzle == "fourth_puzzle":
            current_hint_attempt = 0

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[]

class ActionPickItem(Action):
    def name(self) -> Text:
        return "action_pick_something"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        picked_item = tracker.get_slot("picked_item")
        # print(current_room)
        if not picked_item:
            dispatcher.utter_message(text="There are no items to be picked")
        else:
            dispatcher.utter_message(text=f"You just picked {picked_item}!")
        return []