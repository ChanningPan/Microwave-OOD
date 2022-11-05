import sys
import time
import threading

from abc import ABC, abstractmethod
from food import *


class State(ABC):
    """ Base class of microwave state

        Define open, close, start, stop abstract method for state transition
    """

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass


class OpenState(State):
    """ State class while the door is open

        OpenState can go to CloseState,
        OpenState cannot go to CookState
    """

    def open(self):
        print("The door has already been opened...")
        return self

    def close(self):
        print("Successfully close the door.")
        return CloseState()

    def start(self):
        print("Start Button Forbidden")
        return self

    def stop(self):
        print("Stop Button Forbidden")
        return self


class CloseState(State):
    """ State class while the door is closed

        CloseState can go to both OpenState and CookState
    """

    def open(self):
        print("Successfully open the door.")
        return OpenState()

    def close(self):
        print("The door has already been closed...")
        return self

    def start(self):
        print("Start cooking...")
        return CookState()

    def stop(self):
        print("Stop Button Forbidden")
        return self


class CookState(State):
    """ State class while the microwave is cooking

        CookState can go to CloseState,
        CookState cannot go to OpenState
    """

    def open(self):
        print("\nThe door cannot be opened while cooking!")
        return self

    def close(self):
        print("\nThe door has already been closed...")
        return self

    def start(self):
        print("\nStart Button Forbidden")
        return self

    def stop(self):
        print("Cooking stopped.")
        return CloseState()


class Microwave(object):
    """ Microwave class with basic functionality

        The microwave class support:
        [Basic] Open Door, Close Door, Set Time, Start Cooking, Stop Cooking, Put Food, Take Out Food
        [Advanced] Add 30 seconds, High Power Start

        Attributes:
        _state: current state of the microwave object
        cooking_time_in_sec: preset cooking time, Integer in seconds
        food: food object inside the microwave, None if empty
        temperature_increase_per_sec: Reflect the power of the microwave
    """
    _state = None
    cook_time_in_sec = 0
    food = None
    temperature_increase_per_sec = 0.5

    def __init__(self, state):
        self.transition_to(state)

    @staticmethod
    def sec_to_time(time_in_sec):
        """ Transfer time_in_sec into normal time display xx:xx

        Time is between 0:00 - 59:59

        :param time_in_sec: Integer
        :return: XX:XX : String
        """
        second = str(time_in_sec % 60)
        if len(second) == 1:
            second = '0' + second
        minute = str(time_in_sec // 60)
        return minute + ":" + second

    @property
    def cook_time(self):
        """ Remaining/preset cook time displayed in xx:xx

        :return: XX:XX : String
        """
        return self.sec_to_time(self.cook_time_in_sec)

    def get_state(self):
        """ Get current state of the microwave

        :return: State : String
        """
        return type(self._state).__name__

    def transition_to(self, state):
        """ Transition to state

        :param state: State Object
        :return:
        """
        self._state = state
        self._state.context = self

    def show(self):
        """ Print out current information of the microwave

        :return:
        """
        print("Microwave:" + microwave.get_state())
        print("Preset Cook Time:" + microwave.cook_time)
        if self.food:
            print("Food:" + self.food.name)
        else:
            print("Empty")

    def open_door(self):
        """ Open door

        CloseState -> OpenState
        OpenState -> OpenState
        CookState -> CookState
        :return:
        """
        self.transition_to(self._state.open())

    def put(self, food):
        """ Put food into the microwave

        Food cannot be put if the door is not open!!

        :param food: A food object
        :return:
        """
        if self.get_state() != "OpenState" or self.food:
            print("Cannot put food!")
        else:
            self.food = food
            print("Successfully put " + food.name + "!")

    def close_door(self):
        """ Close door

        OpenState -> CloseState
        CloseState -> CloseState
        CookState -> CookState
        :return:
        """
        self.transition_to(self._state.close())

    def add_30_sec(self):
        """ Add 30 seconds to cook time

        It can be done before start cooking or during the cooking

        :return:
        """
        self.cook_time_in_sec += 30
        print("Current cook time: " + self.cook_time)

    def set_time(self, time_in_second):
        """ Set cook time

        [ToDo] Block it when cooking
        time_in_second should be in a valid range

        :param time_in_second: Integer
        :return:
        """
        if time_in_second.isnumeric() and int(time_in_second) < 60*60:
            self.cook_time_in_sec = int(time_in_second)
            print("Current cook time: " + self.cook_time)
        else:
            print("Invalid time input in seconds!")

    def start(self):
        """ Click Start button to cook

        Even the microwave is empty, it would work
        create a new cook thread different from main thread

        OpenState -> OpenState
        CloseState -> CookState
        CookState -> CookState
        :return:
        """
        self.transition_to(self._state.start())
        if self.get_state() == "CookState":
            thread = threading.Thread(target=self.cook)
            thread.start()

    def high_power_start(self):
        """ Higher Power means larger temperature_increase_per_sec

        :return:
        """
        self.temperature_increase_per_sec = 1
        self.start()
        self.temperature_increase_per_sec = 0.5

    def cook(self):
        """ Cook function

        Use while loop and time.sleep() to implement Countdown
        If loop ends, the cook is completed and state switch to CloseState
        If loop is terminated by stop(), we find current state is not CookState, then return

        :return:
        """
        while self.cook_time_in_sec >= 0:
            # If the Stop button is clicked
            if self.get_state() != "CookState":
                self.cook_time_in_sec = 0
                return
            # Display countdown
            time.sleep(1)
            # Heat food
            if self.food:
                self.food.heat(self.temperature_increase_per_sec)
            sys.stdout.write('\r' + 'Countdown ' + self.cook_time)
            self.cook_time_in_sec -= 1

        # Cook completed and reset cook_time_in_sec to zero
        print("\n\nCook completed!")
        self.cook_time_in_sec = 0
        self.transition_to(CloseState())

    def stop(self):
        """ Click Stop button to terminate

        CookState -> CloseState
        CloseState -> CloseState
        OpenState -> OpenState
        :return:
        """
        self.transition_to(self._state.stop())

    def take_out(self):
        """ Take out food and get information

        If the door is not open or the microwave is empty, the action is invalid

        :return:
        """
        if self.get_state() != "OpenState" or not self.food:
            print("Cannot take out!")
        else:
            self.food.list_all_info()
            self.food = None


if __name__ == '__main__':

    print("Select your action:")
    print("[0]Show State")
    print("[1]Open Door")
    print("[2]Close Door")
    print("[3]Click Start Button")
    print("[4]Click Stop Button")
    print("[5]Set Time")
    print("[6]Add 30 seconds")
    print("[7]Put Food")
    print("[8]Take Out Food")
    print("[9]High Power Heat")

    # Create a microwave object
    microwave = Microwave(CloseState())

    while 1:
        command = input()
        if command == "0":
            microwave.show()
        elif command == "1":
            microwave.open_door()
        elif command == "2":
            microwave.close_door()
        elif command == "3":
            microwave.start()
        elif command == "4":
            microwave.stop()
        elif command == "5":
            microwave.set_time(input("Please type your cook time:"))
        elif command == "6":
            microwave.add_30_sec()
        elif command == "7":
            print("[1]Bread")
            print("[2]Meat")
            print("[3]Milk")
            food_type = input("Please choose a food:")
            if food_type == '1':
                microwave.put(Bread())
            elif food_type == '2':
                microwave.put(Meat())
            elif food_type == '3':
                microwave.put(Milk())
            else:
                print("Please try again!")
        elif command == "8":
            microwave.take_out()
        elif command == "9":
            microwave.high_power_start()
        else:
            print("Please select a valid number(0-9)!")
        print()
