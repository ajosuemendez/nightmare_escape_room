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
    "oxygen_puzzle":["You are currently in a Spaceship during an emergency, ALSO OXYGEN IS VERY IMPORTANT", "It is an item that astronauts have to use when they go out to work", "The Item name start with the letter 'S'"],
    "activate_puzzle": ["Activating Emergency protocols is usually from the cockpit computer, you must activate them ASAP", "Make sure to ACTIVATE the protocols!"],
    "planet_puzzle": ["It is the hottest planet in our solar system", "It is named after a roman goddes, whose functions encompass love, beauty, desire", "The name start with the letter 'V'"],
    "moon_puzzle": ["The natural satellite that orbits Earth", "It is white and fairytales say it is made out of cheese", "It starts with the letter 'M'"]
}

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
        

        if current_puzzle == "east_puzzle":
            current_hint_attempt = tracker.get_slot("east_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0
                
            if current_hint_attempt > 1:
                current_hint_attempt = 1

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("east_puzzle_hint_count", current_hint_attempt + 1)]

        if current_puzzle == "north_puzzle":
            current_hint_attempt = tracker.get_slot("north_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0
                
            if current_hint_attempt > 1:
                current_hint_attempt = 1

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("north_puzzle_hint_count", current_hint_attempt + 1)]

        if current_puzzle == "south_puzzle":
            current_hint_attempt = tracker.get_slot("south_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0
                
            if current_hint_attempt > 1:
                current_hint_attempt = 1

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("south_puzzle_hint_count", current_hint_attempt + 1)]

        if current_puzzle == "oxygen_puzzle":
            current_hint_attempt = tracker.get_slot("oxygen_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0
                
            if current_hint_attempt > 2:
                current_hint_attempt = 2

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("oxygen_puzzle_hint_count", current_hint_attempt + 1)]

        if current_puzzle == "activate_puzzle":
            current_hint_attempt = tracker.get_slot("activate_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0
                
            if current_hint_attempt > 1:
                current_hint_attempt = 1

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("activate_puzzle_hint_count", current_hint_attempt + 1)]

        if current_puzzle == "planet_puzzle":
            current_hint_attempt = tracker.get_slot("planet_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0
                
            if current_hint_attempt > 2:
                current_hint_attempt = 2

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("planet_puzzle_hint_count", current_hint_attempt + 1)]

        if current_puzzle == "moon_puzzle":
            current_hint_attempt = tracker.get_slot("moon_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0
                
            if current_hint_attempt > 2:
                current_hint_attempt = 2

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("moon_puzzle_hint_count", current_hint_attempt + 1)]


class ActionPickItem(Action):
    def name(self) -> Text:
        return "action_pick_something"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        picked_item = tracker.get_slot("picked_item")
        # print(current_room)
        current_puzzle_to_be_solve = tracker.get_slot("current_puzzle_to_solve")

        if current_puzzle_to_be_solve: 
            if picked_item:
                if current_puzzle_to_be_solve == "oxygen_puzzle":
                    if picked_item == "suit":
                        dispatcher.utter_message("Yes! You out on the space suit and you take a deep breath.")
                        return[SlotSet("current_puzzle_to_solve", "activate_puzzle")]
                    else:
                        current_lives = tracker.get_slot("lives")
                        if current_lives:
                            dispatcher.utter_message("You picked the wrong item!")
                            dispatcher.utter_message(text=f"You have lost 1 life! You have {current_lives-1} lives left.")
                            return[SlotSet("lives", current_lives-1)]
                        return[]
            # else:
            #     dispatcher.utter_message("You already have the suit on!!")
            #     return[]

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


class ActionSetRoom(Action):
    def name(self) -> Text:
        return "action_set_room"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_room = tracker.get_slot("current_room")

        if current_room:
            dispatcher.utter_message(f"You are at Tareq Room!")
            dispatcher.utter_message(f"You find yourself in a Space ship during an emergency, Between the flashing lights you can notice the Oxygen levels decreasing rapidly, Everything is floating without control and you also remember to activate the emergency protocols to get the Ship under control.")
            dispatcher.utter_message(f"What do you do??")
            return [SlotSet("current_room", "Tareq_room"), SlotSet("current_puzzle_to_solve", "oxygen_puzzle")]
        else:
            dispatcher.utter_message(f"No room to go to!")
            return[]

class ActionActivatePuzzle(Action):

    def __init__(self):
        self.puzzle_name = "activate_puzzle"

    def name(self) -> Text:
        return "action_activate_puzzle"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        is_puzzle_already_solved = tracker.get_slot("is_planet_puzzle_solved")
        if is_puzzle_already_solved:
            dispatcher.utter_message(text=f"You already activated emergency protocols")
            return []

        current_puzzle_to_be_solve = tracker.get_slot("current_puzzle_to_solve")
        if current_puzzle_to_be_solve:
            if current_puzzle_to_be_solve == "activate_puzzle" or current_puzzle_to_be_solve == "planet_puzzle":
                dispatcher.utter_message("In order to activate the emergency protocols you need to solve the following puzzle")
                dispatcher.utter_message("What is the second planet from the Sun, often referred to as Earth's twin?")
                return[SlotSet("current_puzzle_to_solve", "planet_puzzle")]

        
        current_room = tracker.get_slot("current_room")
        if current_room:
            if current_room != "Tareq_room":
                dispatcher.utter_message("I'm sorry but you have to rephrase your message.")
                return[]


        current_lives = tracker.get_slot("lives")
        if current_lives:
            dispatcher.utter_message("I'm sorry but you can't activate them until you are really ready with your equipment.")
            dispatcher.utter_message(f"You lost precious time and so you lost one life too. You have {current_lives-1} lives left.")
            return [SlotSet("lives", current_lives-1)]

        return[]


class ActionPlanetPuzzle(Action):

    def __init__(self):
        self.puzzle_name = "planet_puzzle"

    def name(self) -> Text:
        return "action_planet_puzzle"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # is_puzzle_already_solved = tracker.get_slot("is_planet_puzzle_solved")
        # if is_puzzle_already_solved:
        #     dispatcher.utter_message(text=f"You already solved the venus puzzle")
        #     return []

        planet_answer = tracker.get_slot("planet_answer")

        current_puzzle_to_be_solve = tracker.get_slot("current_puzzle_to_solve")
        
        if current_puzzle_to_be_solve:
            if current_puzzle_to_be_solve == "planet_puzzle":
                if planet_answer:
                    if planet_answer.lower() == "venus":
                        dispatcher.utter_message("That's correct!")
                        dispatcher.utter_message("However, your best bet is to set a course for earth before you run out of energy and oxygen")
                        dispatcher.utter_message("In order to set a course for earth you need to answer the following question: The celestial body where humans first landed in 1969")
                        return[SlotSet("current_puzzle_to_solve", "moon_puzzle"), SlotSet("is_planet_puzzle_solved", True)]
                    else:
                        current_lives = tracker.get_slot("lives")
                        if current_lives:
                            dispatcher.utter_message("Sorry but that is the wrong answer")
                            dispatcher.utter_message(f"You just lost time, energy and another life. You have {current_lives-1} lives left.")
                            return [SlotSet("lives", current_lives-1)]

            if current_puzzle_to_be_solve == "moon_puzzle":
                if planet_answer:
                    if planet_answer.lower() == "moon":
                        dispatcher.utter_message("That's correct!")
                        dispatcher.utter_message("You take a deep breath and exhale in relief knowing that you are on your way home, the door is unlocked and you go to the next room, your keyword is 'ARE'")
                        return[SlotSet("current_puzzle_to_solve", "till_puzzle"), SlotSet("current_room", "Till_room")]
                    else:
                        current_lives = tracker.get_slot("lives")
                        if current_lives:
                            dispatcher.utter_message("Sorry but that is wrong")
                            dispatcher.utter_message(f"You just lost time, energy and another life. You have {current_lives-1} lives left.")
                            return [SlotSet("lives", current_lives-1)]

        dispatcher.utter_message("Sorry but you have to rephrase your message.")
        return[]