from hero import Hero
import datetime

class Game:
    def __init__(self):
        player_name = input("Введите имя вашего героя: ")
        self.player = Hero(player_name)
        self.computer = Hero("Компьютер")
        self.rounds = 0

    def start(self):
        print(f"\n🛡 Битва начинается между {self.player.name} и {self.computer.name}!\n")
        while self.player.is_alive() and self.computer.is_alive():
            self.rounds += 1
            print(f"\n🔁 Раунд {self.rounds}")
            self.player.attack(self.computer)
            if not self.computer.is_alive():
                print(f"💥 {self.computer.name} побежден! {self.player.name} победил!")
                self.save_result(self.player.name)
                break

            self.computer.attack(self.player)
            if not self.player.is_alive():
                print(f"💥 {self.player.name} побежден! {self.computer.name} победил!")
                self.save_result(self.computer.name)
                break

            print(f"❤️ {self.player.name}: {self.player.health} HP | 🤖 {self.computer.name}: {self.computer.health} HP")

    def save_result(self, winner_name):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result_line = (f"[{now}] Победитель: {winner_name} | "
                       f"Игрок: {self.player.name} | "
                       f"Компьютер: {self.computer.name} | "
                       f"Раундов: {self.rounds}\n")
        with open("results.txt", "a", encoding="utf-8") as file:
            file.write(result_line)
