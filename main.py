from classes import AddressBook, Record, Phone, Birthday, ConsoleView
import pickle

def input_error(func): # декоратор для обробки помилок введення
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError, KeyError, Exception) as e:
            return f'Error: {e}'
    return wrapper

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)

    if not record:
        raise ValueError("Contact not found.")
    
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record and isinstance(record.birthday, Birthday):
        return record.birthday.value
    return "No birthday found."

@input_error
def birthdays(book: AddressBook):
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No upcoming birthdays in the next 7 days."
    
    lines = []
    for item in upcoming:
        lines.append(f"{item['name']} - {item['birthday']}")
    return "\n".join(lines)

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        message = "Contact added."

    else:
        record.add_phone(phone)
    return message

@input_error
def change_phone(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found.")
    
    record.edit_phone(old_phone, new_phone)
    return "Phone number updated."

@input_error
def phone(args, book: AddressBook):
    if not args:
        return "Error: Please provide a contact name."
    
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    
    phones = "; ".join(phone.value for phone in record.phones)
    return f"{name} phones: {phones}"

@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "Address book is empty."
    return "\n".join(str(record) for record in book.data.values())

def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    
    command = parts[0].lower()
    args = parts[1:]
    return command, args


def save_data(book, filename="addressbook.pkl"): # збереження даних у файл
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"): # завантаження даних з файлу
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return AddressBook()


def main():
    book = load_data()
    view = ConsoleView()
    print("Welcome to the assistant bot!")

    while True:
        user_input = view.input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            view.display("Good bye!")
            break

        elif command == "hello":
            view.display("How can I help you?")

        elif command == "add":# додавання контакту
            view.display(add_contact(args, book))

        elif command == "change":#змінити телефон
            view.display(change_phone(args, book))

        elif command == "phone":# отримання телефону
            view.display(phone(args, book))

        elif command == "all":# виведення всіх контактів
            view.display(show_all(book))

        elif command == "add-birthday":# додавання дня народження
            view.display(add_birthday(args, book))

        elif command == "show-birthday":# відображення народження
            view.display(show_birthday(args, book))

        elif command == "birthdays":# відображення найближчих днів народження
            view.display(birthdays(book))

        else:
            view.display("Invalid command.")

if __name__ == "__main__":
    main()