import bot
import pytest


def simulate_inputs(inputs):
    idx = 0

    def read_string():
        nonlocal idx
        s = inputs[idx]
        idx += 1
        return s
    return read_string


def test_hello():
    assert bot.hello(bot.Bot()) == 'How can I help you?'


def test_bot():
    output = []
    inputs = ['hello', 'add John, 1234567899', 'show all', 'add Jane, 9876543200',
              'show all', 'change John, 1357998765', 'show all', 'phone Jane', 'good bye']
    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == [
        'How can I help you?',
        'John is added to Contacts',
        "John: Phones: 1234567899",
        'Jane is added to Contacts',
        "John: Phones: 1234567899\nJane: Phones: 9876543200",
        'Number is changed for John',
        "John: Phones: 1357998765\nJane: Phones: 9876543200",
        '9876543200',
        'Good bye!',
    ]

def test_birthdays(freezer):
    freezer.move_to('2023-05-06')
    output = []
    inputs = ['add John, 1234567899, 13/09/1981', 'days to birthday John', 'add Mary, 1234567890', 'set birthday Mary, 01/03/2003', 'days to birthday Mary', '.']
    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == [
        'John is added to Contacts',
        '130 days',
        'Mary is added to Contacts',
        'Mary was born on 01/03/2003',
        '300 days',
    ]

def test_show_all_iterator():
    output = []
    inputs = ['add John %d, 1234567899' % i for i in range(13)] + ['show all', 'next', 'next', 'next', '.']
    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output[13:] == [
        'John 0: Phones: 1234567899\nJohn 1: Phones: 1234567899\nJohn 2: Phones: 1234567899\nJohn 3: Phones: 1234567899\nJohn 4: Phones: 1234567899',
        'John 5: Phones: 1234567899\nJohn 6: Phones: 1234567899\nJohn 7: Phones: 1234567899\nJohn 8: Phones: 1234567899\nJohn 9: Phones: 1234567899',
        'John 10: Phones: 1234567899\nJohn 11: Phones: 1234567899\nJohn 12: Phones: 1234567899',
        "No more data to scroll"
    ]

def test_next_no_iterator():
    output = []
    inputs = ['next', '.']
    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == ["No scrolling context"]

def test_bot_close():
    output = []
    inputs = ['close']
    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == ['Good bye!']


def test_bot_exit():
    output = []
    inputs = ['exit']
    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == ['Good bye!']


def test_bot_change_not_existing():
    output = []
    inputs = ['change Jack, 1234566789', 'exit']

    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == ["'Jack' doesn't exist", "Good bye!"]


def test_bot_phone_not_existing():
    output = []
    inputs = ['phone Alex', 'exit']

    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == ["'Alex' doesn't exist", "Good bye!"]


def test_bot_show_all_empty():
    output = []
    inputs = ['show all', 'exit']

    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == ["Contact book is empty", "Good bye!"]


def test_bot_dot():
    output = []
    inputs = ['.']

    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == []


def test_bot_unknown_command():
    output = []
    bot.main(read_string=simulate_inputs(
        ['drop John', '.']), print=output.append)
    assert output == ["Please rephrase your command"]


def test_bot_no_args():
    output = []
    bot.main(read_string=simulate_inputs(
        ['add', '.']), print=output.append)
    assert output == [
        'Not enough data for this command, please provide: name, phone']


def test_bot_value_err():
    output = []
    bot.main(read_string=simulate_inputs(
        ['add John, 867594', '.']), print=output.append)
    assert output == ['Please enter a valid phone']


def test_add_phone():
    output = []
    bot.main(read_string=simulate_inputs(
        ['add John, 867594568901', 'add phone John, 98776543981', 'show all', '.']), print=output.append)
    assert output == ['John is added to Contacts',
                      'Number 98776543981 is added to contact John', 'John: Phones: 867594568901, 98776543981']


def test_delete_phone():
    output = []
    bot.main(read_string=simulate_inputs(
        ['add John, 867594568901', 'add phone John, 98776543981', 'delete phone John, 867594568901', 'show all', '.']), print=output.append)
    assert output == ['John is added to Contacts',
                      'Number 98776543981 is added to contact John', 'Number 867594568901 is deleted from contact John', 'John: Phones: 98776543981']
