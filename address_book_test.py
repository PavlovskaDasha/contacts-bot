import address_book
import datetime
import pytest


def test_record():
    name_1 = address_book.Name("Alex")
    phone_1 = address_book.Phone("+380501015455")
    record_1 = address_book.Record(name_1, phone_1)
    assert str(record_1) == "Alex: Phones: 380501015455"

    record_1.add_phone(address_book.Phone("+380665055456"))
    assert str(record_1) == "Alex: Phones: 380501015455, 380665055456"

    record_1.change_phone(
        address_book.Phone("+380665055456"), address_book.Phone("+380991017889")
    )
    assert str(record_1) == "Alex: Phones: 380501015455, 380991017889"

    record_1.delete_phone(address_book.Phone("+380991017889"))
    assert str(record_1) == "Alex: Phones: 380501015455"


def test_double_add():
    name_1 = address_book.Name("Alex")
    phone_1 = address_book.Phone("+380501015455")
    record_1 = address_book.Record(name_1, phone_1)
    contacts = address_book.AddressBook()
    contacts.add_record(record_1)
    with pytest.raises(ValueError):
        contacts.add_record(record_1)


def test_address_book():
    name_1 = address_book.Name("Alex")
    phone_1 = address_book.Phone("+380501015455")
    record_1 = address_book.Record(name_1, phone_1)

    book = address_book.AddressBook()
    book.add_record(record_1)
    assert str(book) == "{<Name: Alex>: Alex, Phones: [<Phone: 380501015455>]}"


def test_birthday_sanitize():
    value = address_book.Birthday("01/03/2014")
    assert value.value == datetime.date(year=2014, month=3, day=1)


@pytest.mark.freeze_time
def test_days_to_birthday(freezer):
    record = address_book.Record(
        address_book.Name("Alex"), birthday=address_book.Birthday("01/03/2014")
    )
    freezer.move_to("2023-03-01")
    assert record.days_to_birthday() == 0
    freezer.move_to("2021-02-28")
    assert record.days_to_birthday() == 1
    freezer.move_to("2020-02-28")
    assert record.days_to_birthday() == 2
    freezer.move_to("2023-03-02")
    assert record.days_to_birthday() == 365


def test_iteration():
    contact_book = address_book.AddressBook()
    assert len(list(contact_book)) == 0
    for i in range(3):
        i = address_book.Record(address_book.Name("name %d" % i))
        contact_book.add_record(i)
    assert len(list(contact_book)[0]) == 3

    for i in range(2):
        i = address_book.Record(address_book.Name("name2 %d" % i))
        contact_book.add_record(i)
    assert len(list(contact_book)[0]) == 5

    for i in range(2):
        i = address_book.Record(address_book.Name("name3 %d" % i))
        contact_book.add_record(i)
    assert len(list(contact_book)[1]) == 2


def test_saving_to_file_pickle():
    address_book_1 = address_book.AddressBook()
    address_book_1.add_record(
        address_book.Record(
            address_book.Name("D"),
            address_book.Phone("9872173665919"),
            address_book.Birthday("23/09/2000"),
        )
    )
    store = address_book.PickleStore("address_book.bin")
    address_book_1.save_to_file(store)
    address_book_2 = address_book.AddressBook()
    address_book_2.read_from_file(store)
    assert address_book_2["D"].phones[0].value == "9872173665919"


def test_delete_phone():
    phone1 = address_book.Phone("123456789091")
    phone2 = address_book.Phone("098764537291")
    name1 = address_book.Name("Alex")
    record1 = address_book.Record(name1, phone1)
    record1.add_phone(phone2)
    record1.delete_phone(phone1)
    assert len(record1.phones) == 1
    with pytest.raises(ValueError):
        record1.delete_phone(phone1)
    assert len(record1.phones) == 1


def test_search_by_phone():
    contact_book = address_book.AddressBook()
    phone1 = address_book.Phone("123456789091")
    phone2 = address_book.Phone("098764537291")
    name1 = address_book.Name("Alex")
    record1 = address_book.Record(name1, phone1)
    record1.add_phone(phone2)
    contact_book.add_record(record1)

    phone = address_book.Phone("098764537291")
    name = address_book.Name("Victor")
    record = address_book.Record(name, phone)
    contact_book.add_record(record)

    assert len(list(contact_book.search_record_by_phone("098764537291"))[0]) == 2
