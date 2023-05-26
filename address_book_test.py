import address_book


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
