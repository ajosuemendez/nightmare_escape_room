from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


# puzzle_prompts = {
#     "date_puzzle" : "I was only 25 years old the day before yesterday and next year I'll be 28. What is the only date this can happen?",
#     "worldcup_puzzle": "What is the Nation with the most Football World Cups?",
#     "wet_puzzle": "What gets wet when drying?",
#     "fourth_puzzle": "There are no riddles to be solved",
#     "east_puzzle": ["I suggest to look around", "you can figure it out from the answer of the previous puzzle!"],
#     "north_puzzle": ["I suggest to look around", "you can figure it out from the answer of the previous puzzle!"],
#     "south_puzzle": ["I suggest to look around", "you can figure it out from the answer of the previous puzzle!",
# }

puzzle_hints = {
    "date_puzzle" : ["It is a date between December and January", "It is closer to the end of the year", "First of...."],
    "worldcup_puzzle": ["It is the largest country in South America", "They speak portuguese in this country", "Bra..."],
    "wet_puzzle": ["You can find this item in your bathroom", "You use it (hopefully) everyday when you take a shower", "To..."],
    "fourth_puzzle": ["There are no hints since there are no puzzles to be solved"],
    "son_puzzle": ["You can have it if you are married", "when they grow up they can become super annoying like Till", "It starts with S and ends with ON"],
    "math_puzzle": ["There is a relation between the actual sum of the numbers and the ones which have been assumed!", "It is easier than you think! The multiplication grows sequentially!", "It is a 3 digit numbers and it start with a 2"],
    "east_puzzle": ["I suggest to look around", "you can figure it out from the answer of the previous puzzle!"],
    "north_puzzle": ["I suggest to look around", "you can figure it out from the answer of the previous puzzle!"],
    "south_puzzle": ["I suggest to look around", "you can figure it out from the answer of the previous puzzle!"],
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
                dispatcher.utter_message(text=f"Hi {name}, Delwan is a young programmer. She was working on a Chabot game while she felt in sleep. Suddenly she heard a voice and woke up, but not in reality!! She found herself in her nightmare. The moment you start playing the game in this room you got stuck in the room with her, she is fuzzy and cannot figure out how to escape this room. You should help her or you both will stay here for everrrrrrrr. First of all you should know that you need a password to open the door but there is a problem!")
                dispatcher.utter_message(text="If you enter the wrong password three times You will get pineapple pizza! ")
                dispatcher.utter_message(text="Be careful and pay attention to every objects that you read about.")
                
                dispatcher.utter_message(text="You have to solve three puzzles to achieve the password! The answer to the first puzzle is the clue for the second one and the second one's answer is the clue for the last one! By solving the last puzzle you will receive the password!")
                dispatcher.utter_message(text="Are you ready to start?")

                return [SlotSet("name", name), SlotSet("current_puzzle_to_solve", "date_puzzle"), SlotSet("lives", 10)]
            else:
                dispatcher.utter_message(text=f"Sorry I don't understand. Can you rephrase it?")
                return []

class ActionAffirmStartGame(Action):

    def name(self) -> Text:
        return "action_handle_affirmation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.get_intent_of_latest_message()

        if intent == "affirm_to_play":
            dispatcher.utter_message("You woke up in the center of the room! On the north you see a window with ocean view (yes that's weird because she is living in the jungle where polar bears are living!) you can enjoy a beautiful sunset there!On the east you see a table with some objects on it. On the south there is door which seems to be the exit door! But a polar bear is sitting next to it and staring at you! On the west you see aboard with some lines written on it and also a broken chair")
            dispatcher.utter_message("Which direction do you want to go?")
        elif intent == "deny_to_play":
            dispatcher.utter_message("I was just being nice! You have no choice! Play or die!")
        else:
            dispatcher.utter_message("I'm sorry, I didn't understand. Can you please clarify?")

        return []

class ActionGiveDirection(Action):

    def name(self) -> Text:
        return "action_handle_direction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        direction = tracker.get_slot("direction")

        if direction:
            if direction == "west":
                is_puzzle_already_solved = tracker.get_slot("is_son_puzzle_solved")
                if is_puzzle_already_solved:
                    dispatcher.utter_message(text=f"You have already solved this puzzle, look around any other part of the room")
                    return []

                dispatcher.utter_message("There is a puzzle on the board")
                dispatcher.utter_message('"Brothers and sisters have I none, but the father of the man is the father of my son, what is his relationship to me?"')
                return [SlotSet("current_puzzle_to_solve", "son_puzzle")]

            if direction == "east":
                is_puzzle_already_solved = tracker.get_slot("is_math_puzzle_solved")
                if is_puzzle_already_solved:
                    dispatcher.utter_message(text=f"You have already solved this puzzle, look around any other part of the room")
                    return []
                dispatcher.utter_message("There are two laptops on the table you are able to select one of them. Be careful! you only have one choice! One of them works with IOS operating system and one of them with windows!")
                return [SlotSet("current_puzzle_to_solve", "east_puzzle")]
            if direction == "north":
                dispatcher.utter_message("You are enjoying a beautiful sunset from the window or maybe windows.")
                return [SlotSet("current_puzzle_to_solve", "north_puzzle")]
            if direction == "south":
                dispatcher.utter_message("The bear next to the door seems to be a doll but it is not!! It has a tiny little red hat with a flower on it! His hand is in his pocket which has a picture of a fish on it!")
                dispatcher.utter_message("What do you want to do?")
                return [SlotSet("current_puzzle_to_solve", "south_puzzle")]
        else:
            dispatcher.utter_message("Sorry try again!")
        return []


# class ActionTurnOn(Action):

#     def name(self) -> Text:
#         return "action_handle_turn_on"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         picked_item = tracker.get_slot("picked_item")
        
#         if picked_item:
#             if picked_item == "laptop" or picked_item == "computer" or picked_item == "notebook":
#                 dispatcher.utter_message("Please select one of the 2 existing types of laptops")
#             elif picked_item.find("ios") != -1:
#                 dispatcher.utter_message("You lost 3 lifes")
#             elif picked_item.lower().find("windows") != -1:
#                 dispatcher.utter_message("You picked the right one!")
#             else:
#                 dispatcher.utter_message(f"You can't turn on the {picked_item}!")
#         else:
#             dispatcher.utter_message(f"There is no item to turn on")
#         return []


class ActionSonPuzzle(Action):
    def __init__(self):
        self.puzzle_name = "son_puzzle"

    def name(self) -> Text:
        return "action_son_puzzle"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        is_puzzle_already_solved = tracker.get_slot("is_son_puzzle_solved")
        if is_puzzle_already_solved:
            dispatcher.utter_message(text=f"You are talking nonsenses")
            return []

        current_puzzle_to_be_solved = tracker.get_slot("current_puzzle_to_solve")

        if current_puzzle_to_be_solved:
            if current_puzzle_to_be_solved != self.puzzle_name:
                dispatcher.utter_message(text=f"Sorry I don't understand. Can you rephrase it?")
                return []

        son_answer = tracker.get_slot("son_answer")

        if son_answer:
            if son_answer.lower() == "son":
                dispatcher.utter_message(text=f'Correct! Remember this answer for the next puzzle')
                dispatcher.utter_message(text=f"Now where do you want to go?")
                return[SlotSet("is_son_puzzle_solved", True)]
            else:
                dispatcher.utter_message(text=f"Wrong answer! Try again!")
        return []

class ActionMathPuzzle(Action):
    def __init__(self):
        self.puzzle_name = "math_puzzle"

    def name(self) -> Text:
        return "action_math_puzzle"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        is_puzzle_already_solved = tracker.get_slot("is_math_puzzle_solved")
        if is_puzzle_already_solved:
            dispatcher.utter_message(text=f"You are talking nonsenses")
            return []

        current_puzzle_to_be_solved = tracker.get_slot("current_puzzle_to_solve")

        if current_puzzle_to_be_solved:
            if current_puzzle_to_be_solved != self.puzzle_name:
                dispatcher.utter_message(text=f"Sorry I don't understand. Can you rephrase it?")
                return []

        math_answer = tracker.get_slot("math_answer")

        if math_answer:
            if math_answer.lower() == "two hundred ninety six" or math_answer == "296":
                dispatcher.utter_message("You see a polar bear on the desktop, It is so cute with a pocket full of fish! (weird!!! Why a bear should have a pocket????)")
                dispatcher.utter_message(text=f"Where do you wanna go now?")
                return[SlotSet("is_math_puzzle_solved", True)]
                # return[]

            else:
                dispatcher.utter_message(text=f"Wrong answer! Try again!")
        return []
            

# class ActionRiddleCheck(Action):

#     def __init__(self):
#         self.possible_corret_answers = ["first of january", "1st january", "01.01", "1 january", "january 1", "january first"]
#         self.already_solved = False
#         self.puzzle_name = "date_puzzle"

#     def name(self) -> Text:
#         return "action_say_is_date_riddle_correct"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         current_puzzle_to_be_solved = tracker.get_slot("current_puzzle_to_solve")

#         if current_puzzle_to_be_solved:
#             if current_puzzle_to_be_solved != self.puzzle_name:
#                 dispatcher.utter_message(text=f"Sorry I don't understand. Can you rephrase it?")
#                 return []

#         answer_date = tracker.get_slot("answer_date")
#         if not answer_date:
#             dispatcher.utter_message(text="Repeat your answer please.")
#             return []

#         else:
#             for answer in self.possible_corret_answers: 
#                 if answer_date.lower() == answer:
#                     dispatcher.utter_message(text=f"The lock fell off and you try to open the door. Unfortunately the door is still locked.")
#                     dispatcher.utter_message(text=f"You see another lock with more inscriptions: What is the Nation with the most Football World Cups?")
#                     self.already_solved = True

#                     puzzles_solved_num = tracker.get_slot("number_puzzle_solved")
#                     if puzzles_solved_num is None:
#                         puzzles_solved_num = 1
#                     else:
#                         puzzles_solved_num += 1

#                     #We have to update we entered to a new room and that we have solved a puzzle
#                     return [SlotSet("number_puzzle_solved", puzzles_solved_num), SlotSet("current_puzzle_to_solve", "worldcup_puzzle")]


            

#             current_lives = tracker.get_slot("lives")
#             if current_lives < 2:
#                 dispatcher.utter_message(text=f"GAME OVER.")
#                 return []

#             dispatcher.utter_message(text=f"The door is still locked...Try again")
#             dispatcher.utter_message(text=f"You have lost a life! You have {current_lives-1} lives left.")


#             return [SlotSet("lives", current_lives-1)]



# class GetCurrentRoomAction(Action):

#     def name(self) -> Text:
#         return "action_get_current_room"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         current_room = tracker.get_slot("current_room")
#         # print(current_room)
#         if not current_room:
#             dispatcher.utter_message(text="You are in the starting room")
#         else:
#             dispatcher.utter_message(text=f"You are in the {current_room}!")
#         return []

# class GetNumberPuzzlesSolvedAction(Action):

#     def name(self) -> Text:
#         return "action_get_number_puzzle_solved"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         number_puzzle_solved = tracker.get_slot("number_puzzle_solved")
#         if not number_puzzle_solved:
#             dispatcher.utter_message(text=f"No puzzles solved.")
#         else:
#             dispatcher.utter_message(text=f"You have solved {number_puzzle_solved} puzzles!")
#         return []

# class GetCurrentPuzzlePromptAction(Action):

#     def name(self) -> Text:
#         return "action_get_current_puzzle_prompt"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         current_puzzle= tracker.get_slot("current_puzzle_to_solve")
#         if not current_puzzle:
#             dispatcher.utter_message(text=f"No puzzles to be solved.")
#         else:
#             dispatcher.utter_message(text=f"{puzzle_prompts[current_puzzle]}")
#         return []

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


# class WorldCupRiddleCheck(Action):
#     def __init__(self):
#         self.puzzle_name = "worldcup_puzzle"

#     def name(self) -> Text:
#         return "action_say_is_world_cup_riddle_correct"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         current_puzzle_to_be_solved = tracker.get_slot("current_puzzle_to_solve")

#         if current_puzzle_to_be_solved:
#             if current_puzzle_to_be_solved != self.puzzle_name:
#                 dispatcher.utter_message(text=f"Sorry I don't understand. Can you rephrase it?")
#                 return []


#         world_cup_answer = tracker.get_slot("answer_world_cup")

#         if world_cup_answer:
#             if world_cup_answer.lower() == "brazil":
#                 dispatcher.utter_message(text=f"The second lock fell off and you try to open the door. Unfortunately the door is still locked.")
#                 dispatcher.utter_message(text=f"You see another lock with more inscriptions: What gets wet when drying?")

#                 puzzles_solved_num = tracker.get_slot("number_puzzle_solved")
#                 if puzzles_solved_num is None:
#                     puzzles_solved_num = 1
#                 else:
#                     puzzles_solved_num += 1
#                 return [SlotSet("number_puzzle_solved", puzzles_solved_num), SlotSet("current_puzzle_to_solve", "wet_puzzle")]

#             else:
                
#                 current_lives = tracker.get_slot("lives")
#                 if current_lives < 2:
#                     dispatcher.utter_message(text=f"GAME OVER.")
#                     return []

#                 dispatcher.utter_message(text=f"Wrong! Try again looser")
#                 dispatcher.utter_message(text=f"You have lost a life! You have {current_lives-1} lives left.")


#                 return [SlotSet("lives", current_lives-1)]

#         dispatcher.utter_message(text=f"I do not understand")

#         return []

# class WetRiddleCheck(Action):
#     def __init__(self):
#         self.puzzle_name = "wet_puzzle"

#     def name(self) -> Text:
#         return "action_say_is_wet_riddle_correct"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         current_puzzle_to_be_solved = tracker.get_slot("current_puzzle_to_solve")

#         if current_puzzle_to_be_solved:
#             if current_puzzle_to_be_solved != self.puzzle_name:
#                 dispatcher.utter_message(text=f"Sorry I don't understand. Can you rephrase it?")
#                 return []


#         wet_answer = tracker.get_slot("answer_wet")

#         if wet_answer:
#             if wet_answer.lower() == "towel" or wet_answer.lower() == "towels":

#                 puzzles_solved_num = tracker.get_slot("number_puzzle_solved")
#                 if puzzles_solved_num is None:
#                     puzzles_solved_num = 1
#                 else:
#                     puzzles_solved_num += 1
                
#                 if puzzles_solved_num == 3:
#                     dispatcher.utter_message(text=f"The third lock has fallen off. You try again to open the door and it opens without much effort.")
#                     dispatcher.utter_message(text=f"Congrats! You made your way out!")
#                     return [SlotSet("number_puzzle_solved", puzzles_solved_num), SlotSet("current_room", "Lobby"), SlotSet("current_puzzle_to_solve", "fourth_puzzle")]

#                 return [SlotSet("number_puzzle_solved", puzzles_solved_num), SlotSet("current_puzzle_to_solve", "fourth_puzzle")]

#             else:
                
#                 current_lives = tracker.get_slot("lives")
#                 if current_lives:
#                     if current_lives < 2:
#                         dispatcher.utter_message(text=f"GAME OVER.")
#                         return []
#                     dispatcher.utter_message(text=f"Wrong! Try again looser")
#                     dispatcher.utter_message(text=f"You have lost a life! You have {current_lives-1} lives left.")


#                 return [SlotSet("lives", current_lives-1)]

#         dispatcher.utter_message(text=f"I do not understand")

#         return []

class GetHints(Action):
    def name(self) -> Text:
        return "action_get_hints"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot("current_puzzle_to_solve") is None:
            dispatcher.utter_message(text="There are no puzzles yet! Please enter your name first!")
            return[]

        current_puzzle = tracker.get_slot("current_puzzle_to_solve")

        if current_puzzle == "son_puzzle":
            current_hint_attempt = tracker.get_slot("son_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0

            if current_hint_attempt > 2:
                current_hint_attempt = 2

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("son_puzzle_hint_count", current_hint_attempt + 1)]

        if current_puzzle == "math_puzzle":
            current_hint_attempt = tracker.get_slot("math_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0

            if current_hint_attempt > 2:
                current_hint_attempt = 2

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("math_puzzle_hint_count", current_hint_attempt + 1)]
        

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

        elif current_puzzle == "east_puzzle":
            current_hint_attempt = tracker.get_slot("east_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0
                
            if current_hint_attempt > 1:
                current_hint_attempt = 1

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("east_puzzle_hint_count", current_hint_attempt + 1)]

        elif current_puzzle == "north_puzzle":
            current_hint_attempt = tracker.get_slot("north_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0
                
            if current_hint_attempt > 1:
                current_hint_attempt = 1

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("north_puzzle_hint_count", current_hint_attempt + 1)]

        elif current_puzzle == "south_puzzle":
            current_hint_attempt = tracker.get_slot("south_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0
                
            if current_hint_attempt > 1:
                current_hint_attempt = 1

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("south_puzzle_hint_count", current_hint_attempt + 1)]


class ActionPickItem(Action):
    def name(self) -> Text:
        return "action_pick_something"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        picked_item = tracker.get_slot("picked_item")
        # print(current_room)
        if picked_item:
            if picked_item == "laptop" or picked_item == "computer" or picked_item == "notebook":
                dispatcher.utter_message("Please select one of the 2 existing types of laptops! (Ios or Windows)")

            elif picked_item.find("ios") != -1:
                current_lives = tracker.get_slot("lives")
                if current_lives:
                    if current_lives < 2:
                        dispatcher.utter_message(text=f"GAME OVER.")
                        return []
                    dispatcher.utter_message("You picked the wrong one!")
                    dispatcher.utter_message(text=f"You have lost 3 life! You have {current_lives-3} lives left.")
                    return [SlotSet("lives", current_lives-3)]

            elif picked_item.lower().find("windows") != -1:
                dispatcher.utter_message("You can see a puzzle on the screen saver, solve it to turn it on!")
                dispatcher.utter_message("according to the first three equations, try to find the answer to the fourth one: 21+10=31\n22+20=84\n23+30=159\n24+50=?")
                return [SlotSet("current_puzzle_to_solve", "math_puzzle")]
            else:
                dispatcher.utter_message(f"You just picked {picked_item}!")
        else:
            dispatcher.utter_message(f"No Item was picked")

        return []


class ActionLookItem(Action):
    def name(self) -> Text:
        return "action_look_at"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        looked_item = tracker.get_slot("looked_item")

        if looked_item:
            dispatcher.utter_message(f"You are looking at the {looked_item}")
        else:
            dispatcher.utter_message(f"There is nothing to look at")
        return []