import random
from abc import ABC, abstractmethod


# Weapon Interface
class Weapon(ABC):
    @abstractmethod
    def attack(self) -> int:
        """Возвращает количество урона"""
        pass


# Concrete Weapons
class Sword(Weapon):
    def attack(self):
        damage = random.randint(15, 30)
        print(f"⚔️ Меч наносит {damage} урона.")
        return damage


class Bow(Weapon):
    def attack(self):
        damage = random.randint(10, 25)
        print(f"🏹 Лук наносит {damage} урона.")
        return damage


class Axe(Weapon):
    def attack(self):
        damage = random.randint(20, 35)
        print(f"🪓 Топор наносит {damage} урона.")
        return damage


# Fighter
class Fighter:
    def __init__(self, name):
        self.name = name
        self.weapon: Weapon = None
        self.experience = 0

    def change_weapon(self, weapon: Weapon):
        self.weapon = weapon
        print(f"{self.name} выбирает {weapon.__class__.__name__}")

    def gain_experience(self, points: int):
        self.experience += points
        print(f"🌟 {self.name} получает {points} XP! Общий опыт: {self.experience}")

    def attack(self, monster):
        if not self.weapon:
            print("❗ Нет оружия!")
            return
        damage = self.weapon.attack()
        monster.take_damage(damage)
        self.gain_experience(damage)


# Monster
class Monster:
    def __init__(self, name):
        self.name = name
        self.health = random.randint(60, 120)

    def take_damage(self, damage: int):
        self.health -= damage
        print(f"💥 {self.name} получает {damage} урона. Осталось HP: {max(self.health, 0)}")
        if self.health <= 0:
            print(f"☠️ {self.name} побежден!")

    def is_alive(self) -> bool:
        return self.health > 0


# Weapon Factory
def get_weapon_by_choice(choice: str):
    weapons = {
        "sword": Sword,
        "bow": Bow,
        "axe": Axe
    }
    weapon_class = weapons.get(choice.lower())
    return weapon_class() if weapon_class else None


# Game Loop
def game():
    print("🎮 Добро пожаловать в игру! Выбор оружия: sword, bow, axe")

    fighter = Fighter("Герой")
    monster = Monster("Гоблин")

    print(f"🧟 Противник: {monster.name}, HP: {monster.health}")

    while monster.is_alive():
        choice = input("🔫 Выберите оружие или нажмите Enter для продолжения: ").strip()
        if choice:
            weapon = get_weapon_by_choice(choice)
            if weapon:
                fighter.change_weapon(weapon)
            else:
                print("❌ Оружие не найдено.")
                continue
        fighter.attack(monster)

    print(f"\n🎉 Победа! Итоговый опыт: {fighter.experience} XP")


if __name__ == "__main__":
    game()
