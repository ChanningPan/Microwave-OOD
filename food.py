class Food:
    """ Base class of food

        Attributes:
        name: Food name
        temperature: Thermodynamic temperature, normal is 300K

        Methods:
        heat: heat the food by incremental
    """
    _temperature = 300  # T(K), normal temperature

    def __init__(self):
        pass

    def name(self):
        pass

    @property
    def temperature(self):
        return self._temperature

    def heat(self, incremental):
        """ temperature increased by incremental

        :param incremental: Float
        :return:
        """
        self._temperature += incremental


class Bread(Food):

    @property
    def name(self):
        return "BREAD"

    def list_all_info(self):
        print("Food: " + self.name)
        print("Temperature: " + str(self.temperature - 273) + " Celsius")


class Meat(Food):

    @property
    def name(self):
        return "MEAT"

    def list_all_info(self):
        print("Food: " + self.name)
        print("Temperature: " + str(self.temperature - 273) + " Celsius")


class Milk(Food):

    @property
    def name(self):
        return "MILK"

    def list_all_info(self):
        print("Food: " + self.name)
        print("Temperature: " + str(self.temperature - 273) + " Celsius")
