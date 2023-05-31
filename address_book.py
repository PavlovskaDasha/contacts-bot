from collections import UserDict
import datetime
import pickle
import os
import os.path


class ValidationError(Exception):
    def __init__(self, Field, message):
        self.field = Field.__name__.lower()
        self.message = message


class Field:
    def __init__(self, value=None):
        self.value = value

    @property
    def value(self):
        return self.__value

    def sanitize(self, value: str) -> str:
        return value

    def validate(self, value: str):
        return

    @value.setter
    def value(self, value):
        value = self.sanitize(value)
        self.validate(value)
        self.__value = value

    def __hash__(self) -> int:
        return hash(self.__value)

    def __eq__(self, other) -> bool:
        if hasattr(other, "value"):
            return self.value == other.value
        return self.value == other

    def __str__(self) -> str:
        return self.__value

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.value}>"

    def __contains__(self, value):
        return value in self.value


class Name(Field):
    pass


class Phone(Field):
    def validate(self, value: str):
        if len(value) < 10:
            raise ValidationError(
                Phone,
                f"Length of the phone should be greater than 10. Your phone has only {len(value)} digits",
            )

    def sanitize(self, phone):
        new_phone = (
            phone.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        return new_phone


class Birthday(Field):
    def sanitize(self, value: str) -> datetime.date:
        try:
            return datetime.datetime.strptime(value, "%d/%m/%Y").date()
        except Exception as e:
            raise ValidationError(Birthday, str(e))


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        if not old_phone:
            idx = 0
        else:
            idx = self.phones.index(old_phone)
        self.phones[idx] = new_phone

    def delete_phone(self, phone: Phone):
        try:
            self.phones.remove(phone)
        except:
            raise ValueError("Phone number doesn't exist")

    def set_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def delete_birthday(self):
        self.birthday = None

    def days_to_birthday(self):
        if not self.birthday:
            raise ValueError(f"Birthday is not defined for {self.name}")
        today = datetime.datetime.now().date()
        birthday = self.birthday.value.replace(year=today.year)
        if birthday >= today:
            difference = (birthday - today).days
        else:
            difference = (self.birthday.value.replace(year=today.year + 1) - today).days
        return difference

    def __str__(self) -> str:
        phones = ", ".join([str(phone) for phone in self.phones])
        if self.birthday != None:
            return f'{self.name}: Phones: {phones}, Birthday: {self.birthday.value.strftime("%d/%m/%Y")}'
        return f"{self.name}: Phones: {phones}"

    def __repr__(self) -> str:
        if self.birthday != None:
            return f'{self.name}, Phones: {self.phones}, Birthday: {self.birthday.value.strftime("%d/%m/%Y")}'
        return f"{self.name}, Phones: {self.phones}"

    def match(self, input):
        if input in self.name:
            return True
        for phone in self.phones:
            if input in phone:
                return True
        return False


class PaginationIterator:
    def __init__(self, iterator, N=5):
        self.iterator = iterator
        self.N = N

    def __next__(self):
        values = []
        for i in range(self.N):
            try:
                values.append(next(self.iterator))
            except StopIteration:
                if values:
                    return values
                raise StopIteration
        return values


class AddressBookView:
    def __init__(self, iter):
        self.iter = iter

    def __iter__(self):
        return PaginationIterator(self.iter)


class AddressBook(UserDict[Name, Record]):
    def add_record(self, record: Record):
        if record.name in self.data:
            raise ValueError(f"{record.name} already exists")
        self.data[record.name] = record

    def delete_record(self, name: Name):
        self.data.pop(name)

    def get_record(self, name: Name) -> Record:
        return self.data[name]

    def search_record_by_phone(self, phone: Phone) -> AddressBookView:
        return AddressBookView(filter(lambda x: phone in x.phones, self.data.values()))

    def save_to_file(self, store):
        store.dump(self.data)

    def read_from_file(self, store):
        self.data = store.load()

    def search(self, value: str):
        return AddressBookView(filter(lambda x: x.match(value), self.data.values()))

    def __iter__(self):
        return PaginationIterator(iter(self.data.values()))


class Store:
    pass


class PickleStore(Store):
    def __init__(self, file):
        self.file = file

    def dump(self, data):
        with open(self.file, "wb") as fh:
            pickle.dump(data, fh)
        return

    def load(self) -> AddressBook:
        if os.path.exists(self.file):
            try:
                with open(self.file, "rb") as fh:
                    return pickle.load(fh)
            except:
                os.remove(self.file)
                return {}
        return {}
