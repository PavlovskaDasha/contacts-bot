import bot


def simulate_inputs(inputs):
    idx = 0

    def read_string():
        nonlocal idx
        s = inputs[idx]
        idx += 1
        return s
    return read_string


def test_hello():
    assert bot.hello([]) == 'How can I help you?'


def test_bot():
    output = []
    inputs = ['hello', 'add John 1234567899', 'add Jane 9876543200',
              'show all', 'change John 1357998765', 'show all', 'phone Jane', 'good bye']
    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == [
        'How can I help you?',
        'John is added to Contacts',
        'Jane is added to Contacts',
        'John: 1234567899\nJane: 9876543200',
        'Number is changed for John',
        'John: 1357998765\nJane: 9876543200',
        '9876543200',
        'Good bye!',
    ]


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
    inputs = ['change Jack 1234566789', 'exit']

    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == ["'Jack' doesn't exist", "Good bye!"]


def test_bot_phone_not_existing():
    output = []
    inputs = ['phone Alex', 'exit']

    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == ["'Alex' doesn't exist", "Good bye!"]


def test_bot_show_all_empty():
    bot.Contact_book = {}
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
    assert output == ["Not enough data for this command"]


def test_bot_value_err():
    output = []
    bot.main(read_string=simulate_inputs(
        ['add John 867594', '.']), print=output.append)
    assert output == ['Please enter a valid phone']
