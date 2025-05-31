class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        print(f"{self.name} издаёт звук.")

    def eat(self):
        print(f"{self.name} ест.")


class Bird(Animal):
    def __init__(self, name, age, can_fly=True):
        super().__init__(name, age)
        self.can_fly = can_fly

    def make_sound(self):
        print(f"{self.name} щебечет.")

class Mammal(Animal):
    def __init__(self, name, age, fur_color="brown"):
        super().__init__(name, age)
        self.fur_color = fur_color

    def make_sound(self):
        print(f"{self.name} рычит.")

class Reptile(Animal):
    def __init__(self, name, age, is_venomous=False):
        super().__init__(name, age)
        self.is_venomous = is_venomous

    def make_sound(self):
        print(f"{self.name} шипит.")


# полиморфизм
def animal_sound(animals):
    for animal in animals:
        animal.make_sound()


# Zoo с композицией
class Zoo:
    def __init__(self, name):
        self.name = name
        self.animals = []
        self.staff = []

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"{animal.name} добавлен в зоопарк.")

    def add_staff(self, employee):
        self.staff.append(employee)
        print(f"{employee.name} принят на работу.")


# Классы сотрудников
class Staff:
    def __init__(self, name):
        self.name = name

class ZooKeeper(Staff):
    def feed_animal(self, animal):
        print(f"{self.name} кормит {animal.name}.")
        animal.eat()

class Veterinarian(Staff):
    def heal_animal(self, animal):
        print(f"{self.name} лечит {animal.name}.")


# сохранение и загрузка данных
import json

class ZooEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Animal):
            return {
                "__type__": obj.__class__.__name__,
                "name": obj.name,
                "age": obj.age,
                "__dict__": obj.__dict__
            }
        elif isinstance(obj, Staff):
            return {
                "__type__": obj.__class__.__name__,
                "name": obj.name
            }
        return super().default(obj)

def zoo_decoder(obj):
    if "__type__" in obj:
        type_name = obj["__type__"]
        if type_name == "Bird":
            return Bird(obj["name"], obj["age"], obj["__dict__"]["can_fly"])
        elif type_name == "Mammal":
            return Mammal(obj["name"], obj["age"], obj["__dict__"]["fur_color"])
        elif type_name == "Reptile":
            return Reptile(obj["name"], obj["age"], obj["__dict__"]["is_venomous"])
        elif type_name == "ZooKeeper":
            return ZooKeeper(obj["name"])
        elif type_name == "Veterinarian":
            return Veterinarian(obj["name"])
    return obj

def save_zoo(zoo, filename):
    data = {
        "name": zoo.name,
        "animals": zoo.animals,
        "staff": zoo.staff
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, cls=ZooEncoder, ensure_ascii=False, indent=4)

def load_zoo(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    zoo = Zoo(data["name"])
    zoo.animals = [zoo_decoder(animal) for animal in data["animals"]]
    zoo.staff = [zoo_decoder(employee) for employee in data["staff"]]
    return zoo


# Пример использования
if __name__ == "__main__":
    zoo = Zoo("Мир животных")

    # Добавим животных
    zoo.add_animal(Bird("Попугай", 2))
    zoo.add_animal(Mammal("Тигр", 5, fur_color="оранжевый"))
    zoo.add_animal(Reptile("Кобра", 3, is_venomous=True))

    # Добавим сотрудников
    keeper = ZooKeeper("Андрей")
    vet = Veterinarian("Мария")
    zoo.add_staff(keeper)
    zoo.add_staff(vet)

    # Взаимодействие
    keeper.feed_animal(zoo.animals[0])
    vet.heal_animal(zoo.animals[2])

    # Звук животных
    animal_sound(zoo.animals)

    # Сохраняем состояние
    save_zoo(zoo, "zoo_data.json")

    # Загружаем
    new_zoo = load_zoo("zoo_data.json")
    print(f"Зоопарк загружен: {new_zoo.name}")