from collections import UserDict


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

    def __str__(self) -> str:
        return self.__value

    def __eq__(self, other) -> bool:
        return self.value == other

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: {self.value}'


class Name(Field):
    pass


class Phone(Field):

    def validate(self, value: str):
        if len(value) < 10:
            raise ValueError(f"phone")

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


class FieldSet:
    def __init__(self):
        self.set = set[Field]()

    def add(self, field: Field):
        self.set.add(field)

    def remove(self, field: Field):
        self.set.remove(field)


class Record:

    def __init__(self, name: Name, phone: Phone = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        for phone in self.phones:
            if phone == old_phone:
                phone.value = new_phone.value

    def delete_phone(self, phone: Phone):
        self.phones.remove(phone)

    def __str__(self) -> str:
        phones = ', '.join([str(phone) for phone in self.phones])
        return f'{self.name}: Phones: {phones}'

    def __repr__(self) -> str:
        return f'{self.name}, Phones: {self.phones}'


class AddressBook(UserDict[str, Record]):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def change_phone(self, name: Name, phone: Phone):
        old_phone = self.data[name.value].phones[0]
        self.data[name.value].change_phone(old_phone, phone)
