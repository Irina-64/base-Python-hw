class Store():
     def __init__(self, name, address):
         self.name = name
         self.address = address
         self.items = {}

     def add_item(self, item_name, price):
         self.items[item_name] = price
         print(f"товар {item_name} был добавлен в {self.name}")

     def remove_item(self, item_name):
         if item_name in self.items:
             del self.items[item_name]
             print(f"товар {item_name} удален из {self.name}")

     def get_price(self, item_name):
         return self.items.get(item_name)

     def update_price(self, item_name, new_price):
         if item_name in self.items:
             self.items[item_name] = new_price
             print(f"цена на товар {item_name} обновлена в {self.name}")
         else:
             print(f"товар {item_name} не найден")

store1 = Store("пятерочка", "Ленина 40")
store2 = Store("магнит", "Ленина 45")
store3 = Store("ярче", "Ленина 80")

store1.add_item("хлеб", 67)
store1.add_item("молоко", 120)
store1.add_item("гречка", 60)

store1.remove_item("хлеб")
print(store1.get_price("молоко"))

store1.update_price("гречка", 80)
