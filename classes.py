from collections import UserDict
from datetime import datetime, timedelta


class Field: # базовий клас
    def __init__(self, value):
        self.value = value

    def __str__(self): # метод для виведення значення
        return str(self.value)



class Name(Field): # клас для імені
    def __init__(self, value: str):
        self._validate(value)
        formatted = value.strip()
        super().__init__(formatted)

    def _validate(self, value): # метод для валідації імені
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if not value.strip():
            raise ValueError("Name cannot be empty")
        if not value.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters and spaces")



class Phone(Field): # клас для телефону
    def __init__(self, value):
         super().__init__(value)
         self._validate(value)

    def _validate(self, value): # метод для валідації телефону
        if not isinstance(value, str):
            raise ValueError("Phone number must be a string")
        if len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits long")
              


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        


class Record: # клас для запису контакту
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday_str: str):
        self.birthday = Birthday(birthday_str)

    def add_phone(self, phone_str: str):
        phone = Phone(phone_str)
        self.phones.append(phone)

    def remove_phone(self, phone_str: str): # метод для видалення телефону
        phone = self.find_phone(phone_str)
        if phone:
            self.phones.remove(phone)
        else:
            raise ValueError("Phone not found")

    def edit_phone(self, old_phone_str: str, new_phone_str: str): # метод для редагування телефону
        old = self.find_phone(old_phone_str)

        if old is None:
            raise ValueError("Old phone not found")
        
        self.remove_phone(old_phone_str)
        self.add_phone(new_phone_str)

    def find_phone(self, phone_str: str): # метод для пошуку телефону
        for p in self.phones:
            if p.value == phone_str:
                return p
        return None

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        b_day = f", Birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name}, phones: {phones}{b_day}"



class AddressBook(UserDict): # клас для адресної книги
    def add_record(self, record: Record): # метод для додавання запису
        self.data[record.name.value] = record
    
    def find(self, name: str): # метод для пошуку запису
        if name not in self.data:
            return None
        return self.data.get(name)
    
    def delete(self, name: str): # метод для видалення запису
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        end_date = today + timedelta(days=7)
        result = []

        for record in self.data.values():
            if record.birthday:
                # Конвертуємо рядок у дату
                bday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()

                # Змінюємо рік на поточний, щоб порівняти з today
                bday_this_year = bday_date.replace(year=today.year)

                # Якщо день народження вже був цього року — беремо наступний рік
                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)

                # Якщо день народження у проміжку між today і end_date
                if today <= bday_this_year <= end_date:
                    # Якщо це вихідний — переносимо на понеділок
                    if bday_this_year.weekday() >= 5:  # 5 = субота, 6 = неділя
                        bday_this_year += timedelta(days=(7 - bday_this_year.weekday()))
                    result.append({"name": record.name.value, "birthday": bday_this_year.strftime("%d.%m.%Y")})

        return result

    
    def __str__(self): # метод для виведення адресної книги
        return '\n'.join(str(record) for record in self.data.values())