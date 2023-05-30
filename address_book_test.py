import address_book
import datetime
import pytest


def test_record():
    name_1 = address_book.Name('Alex')
    phone_1 = address_book.Phone('+380501015455')
    record_1 = address_book.Record(name_1, phone_1)
    assert str(record_1) == 'Alex: Phones: 380501015455'

    record_1.add_phone(address_book.Phone('+380665055456'))
    assert str(
        record_1) == 'Alex: Phones: 380501015455, 380665055456'

    record_1.change_phone(address_book.Phone(
        '+380665055456'), address_book.Phone('+380991017889'))
    assert str(
        record_1) == 'Alex: Phones: 380501015455, 380991017889'

    record_1.delete_phone(address_book.Phone('+380991017889'))
    assert str(record_1) == 'Alex: Phones: 380501015455'


def test_address_book():
    name_1 = address_book.Name('Alex')
    phone_1 = address_book.Phone('+380501015455')
    record_1 = address_book.Record(name_1, phone_1)

    book = address_book.AddressBook()
    book.add_record(record_1)
    assert str(book) == "{'Alex': Alex, Phones: [Phone: 380501015455]}"


def test_birthday_sanitize():
    value = address_book.Birthday('01/03/2014')
    assert value.value == datetime.date(year=2014, month=3, day=1)

@pytest.mark.freeze_time
def test_days_to_birthday(freezer):
    record = address_book.Record(address_book.Name('Alex'), birthday=address_book.Birthday("01/03/2014"))
    freezer.move_to('2023-03-01')
    assert record.days_to_birthday() == 0
    freezer.move_to('2021-02-28')
    assert record.days_to_birthday() == 1
    freezer.move_to('2020-02-28')
    assert record.days_to_birthday() == 2
    freezer.move_to('2023-03-02')
    assert record.days_to_birthday() == 365

def test_iteration():
    contact_book=address_book.AddressBook()
    assert len(list(contact_book)) == 0
    for i in range (3):
        i=address_book.Record(address_book.Name('name %d'%i))
        contact_book.add_record(i)
    assert len(list(contact_book)[0]) == 3
    
    for i in range (2):
        i=address_book.Record(address_book.Name('name2 %d'%i))
        contact_book.add_record(i)
    assert len(list(contact_book)[0]) == 5

    for i in range (2):
        i=address_book.Record(address_book.Name('name3 %d'%i))
        contact_book.add_record(i)
    assert len(list(contact_book)[1]) == 2

def test_saving_to_file():
    address_book_1=address_book.AddressBook()
    r = address_book.Record(address_book.Name('D'), address_book.Phone('9872173665919'), address_book.Birthday('23/09/2000'
    ))
    r.add_phone('9872173665932')
    address_book_1.add_record(r)
    address_book_1.add_record(address_book.Record(address_book.Name('E')))

    address_book_1.save_to_file('address_book.json')
    address_book_2=address_book.AddressBook()
    address_book_2.read_from_file('address_book.json')
    assert address_book_2['D'].phones[0].value=='9872173665919'
    assert address_book_2['D'].phones[1].value=='9872173665932'
    assert address_book_2['E'].name.value=='E'

def test_saving_to_file_pickle():
    address_book_1=address_book.AddressBook()
    address_book_1.add_record(address_book.Record(address_book.Name('D'), address_book.Phone('9872173665919'), address_book.Birthday('23/09/2000'
    )))
    address_book_1.save_to_file('address_book.bin')
    address_book_2=address_book.AddressBook()
    address_book_2.read_from_file('address_book.bin')
    assert address_book_2['D'].phones[0].value=='9872173665919'


    

    

