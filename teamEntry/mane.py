import json

class User:
    def __init__(self, user_id, name):
        self.__id = user_id
        self.__name = name
        self.__access_level = 'user'

    # Геттеры
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_access_level(self):
        return self.__access_level

    # Сеттеры
    def set_name(self, name):
        self.__name = name

    def to_dict(self):
        return {
            'id': self.__id,
            'name': self.__name,
            'access_level': self.__access_level
        }

    @staticmethod
    def from_dict(data):
        user = User(data['id'], data['name'])
        return user


class Admin(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.__admin_access_level = 'admin'

    def get_admin_access_level(self):
        return self.__admin_access_level

    def add_user(self, user_list, user):
        if isinstance(user, User):
            user_list.append(user)
            print(f"[+] Пользователь '{user.get_name()}' добавлен.")
        else:
            print("[!] Невозможно добавить: объект не является экземпляром User.")

    def remove_user(self, user_list, user_id):
        for user in user_list:
            if user.get_id() == user_id:
                user_list.remove(user)
                print(f"[-] Пользователь с ID {user_id} удалён.")
                return
        print(f"[!] Пользователь с ID {user_id} не найден.")

    def to_dict(self):
        return {
            'id': self.get_id(),
            'name': self.get_name(),
            'access_level': self.__admin_access_level
        }

    @staticmethod
    def from_dict(data):
        return Admin(data['id'], data['name'])


# --- Работа с файлами ---
def save_users(user_list, filename='users.json'):
    data = [u.to_dict() for u in user_list]
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print("[💾] Пользователи сохранены.")


def load_users(filename='users.json'):
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
        users = []
        for item in data:
            if item['access_level'] == 'admin':
                users.append(Admin.from_dict(item))
            else:
                users.append(User.from_dict(item))
        print("[📥] Пользователи загружены.")
        return users
    except FileNotFoundError:
        print("[⚠️] Файл не найден. Создан пустой список.")
        return []


# --- Авторизация ---
def authorize(user_list, name):
    for user in user_list:
        if user.get_name() == name:
            return user
    return None


# --- Пример использования ---
if __name__ == "__main__":
    users = load_users()

    print("Введите имя для авторизации:")
    login_name = input("Имя: ")
    current_user = authorize(users, login_name)

    if current_user:
        print(f"Добро пожаловать, {current_user.get_name()}! Уровень доступа: {current_user.get_access_level()}")
        if isinstance(current_user, Admin):
            while True:
                print("\n1. Добавить пользователя\n2. Удалить пользователя\n3. Показать всех\n4. Сохранить и выйти")
                choice = input("Выбор: ")
                if choice == '1':
                    new_id = int(input("ID нового пользователя: "))
                    new_name = input("Имя: ")
                    users.append(User(new_id, new_name))
                elif choice == '2':
                    del_id = int(input("ID для удаления: "))
                    current_user.remove_user(users, del_id)
                elif choice == '3':
                    for u in users:
                        print(f"- {u.get_name()} ({u.get_access_level()})")
                elif choice == '4':
                    save_users(users)
                    break
        else:
            print("У вас нет прав администратора.")
    else:
        print("Пользователь не найден.")
