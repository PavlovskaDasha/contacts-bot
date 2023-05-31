import bot
import pytest
import os
import os.path


@pytest.fixture(autouse=True)
def remove_saved_contacts():
    if os.path.isfile("contacts.json"):
        os.remove("contacts.json")
    if os.path.isfile("contacts.bin"):
        os.remove("contacts.bin")


def simulate_inputs(inputs):
    idx = 0

    def read_string():
        nonlocal idx
        if idx >= len(inputs):
            return "."
        s = inputs[idx]
        idx += 1
        return s

    return read_string


def test_hello():
    assert bot.hello(bot.Bot()) == "How can I help you?"


def test_bot():
    output = []
    inputs = [
        "hello",
        "add John, 1234567899",
        "show all",
        "add Jane, 9876543200",
        "show all",
        "change John, 1357998765",
        "show all",
        "phone Jane",
        "good bye",
    ]
    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == [
        "How can I help you?",
        "John is added to Contacts",
        "John: Phones: 1234567899",
        "Jane is added to Contacts",
        "John: Phones: 1234567899\nJane: Phones: 9876543200",
        "Number is changed for John",
        "John: Phones: 1357998765\nJane: Phones: 9876543200",
        "9876543200",
        "Good bye!",
    ]


def test_birthdays(freezer):
    freezer.move_to("2023-05-06")
    output = []
    inputs = [
        "add John, 1234567899, 13/09/1981",
        "days to birthday John",
        "add Mary, 1234567890",
        "set birthday Mary, 01/03/2003",
        "days to birthday Mary",
        ".",
    ]
    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == [
        "John is added to Contacts",
        "130 days",
        "Mary is added to Contacts",
        "Mary was born on 01/03/2003",
        "300 days",
    ]


def test_show_all_iterator():
    output = []
    inputs = ["add John %d, 1234567899" % i for i in range(13)] + [
        "show all",
        "next",
        "next",
        "next",
        ".",
    ]
    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output[13:] == [
        "John 0: Phones: 1234567899\nJohn 1: Phones: 1234567899\nJohn 2: Phones: 1234567899\nJohn 3: Phones: 1234567899\nJohn 4: Phones: 1234567899",
        "John 5: Phones: 1234567899\nJohn 6: Phones: 1234567899\nJohn 7: Phones: 1234567899\nJohn 8: Phones: 1234567899\nJohn 9: Phones: 1234567899",
        "John 10: Phones: 1234567899\nJohn 11: Phones: 1234567899\nJohn 12: Phones: 1234567899",
        "No more data to scroll",
    ]


def test_next_no_iterator():
    output = []
    inputs = ["next", "."]
    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == ["No scrolling context"]


def test_bot_close():
    output = []
    inputs = ["close"]
    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == ["Good bye!"]


def test_bot_exit():
    output = []
    inputs = ["exit"]
    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == ["Good bye!"]


def test_bot_change_not_existing():
    output = []
    inputs = ["change Jack, 1234566789", "exit"]

    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == ["<Name: Jack> doesn't exist", "Good bye!"]


def test_bot_phone_not_existing():
    output = []
    inputs = ["phone Alex", "exit"]

    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == ["<Name: Alex> doesn't exist", "Good bye!"]


def test_bot_show_all_empty():
    output = []
    inputs = ["show all", "exit"]

    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == ["Contact book is empty", "Good bye!"]


def test_bot_dot():
    output = []
    inputs = ["."]

    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output == []


def test_bot_unknown_command():
    output = []
    bot.main(read_string=simulate_inputs(["drop John", "."]), print=output.append)
    assert output == ["Please rephrase your command"]


def test_bot_no_args():
    output = []
    bot.main(read_string=simulate_inputs(["add", "."]), print=output.append)
    assert output == ["Not enough data for this command, please provide: name, phone"]


def test_bot_value_err():
    output = []
    bot.main(
        read_string=simulate_inputs(
            ["add John, 867594", "add John, 09876554318298, 12.04.2003", "."]
        ),
        print=output.append,
    )
    assert output == [
        "Please enter valid phone: Length of the phone should be greater than 10. Your phone has only 6 digits",
        "Please enter valid birthday: time data '12.04.2003' does not match format '%d/%m/%Y'",
    ]


def test_add_phone():
    output = []
    bot.main(
        read_string=simulate_inputs(
            ["add John, 867594568901", "add phone John, 98776543981", "show all", "."]
        ),
        print=output.append,
    )
    assert output == [
        "John is added to Contacts",
        "Number 98776543981 is added to contact John",
        "John: Phones: 867594568901, 98776543981",
    ]


def test_delete_phone():
    output = []
    bot.main(
        read_string=simulate_inputs(
            [
                "add John, 867594568901",
                "add phone John, 98776543981",
                "delete phone John, 867594568901",
                "show all",
                ".",
            ]
        ),
        print=output.append,
    )
    assert output == [
        "John is added to Contacts",
        "Number 98776543981 is added to contact John",
        "Number 867594568901 is deleted from contact John",
        "John: Phones: 98776543981",
    ]


def test_save_load():
    output = []
    bot.main(
        read_string=simulate_inputs(
            ["add John, 867594568901", "add phone John, 98776543981", "show all", "."]
        ),
        print=output.append,
    )
    output = []
    bot.main(
        read_string=simulate_inputs(["phone John", "show all", "."]),
        print=output.append,
    )
    assert output == [
        "867594568901, 98776543981",
        "John: Phones: 867594568901, 98776543981",
    ]


def test_save_load_invalid():
    with open("contacts.json", "w") as f:
        f.write("Invalid")
    output = []
    bot.main(read_string=simulate_inputs(["show all", "."]), print=output.append)
    assert output == ["Contact book is empty"]


def test_search():
    output = []
    inputs = (
        ["add John%d %d, 123456789%d" % (i % 5, i, i % 5) for i in range(100)]
        + ["search 1234567894", "next", "next", "next", "next"]
        + ["search John0", "next", "next", "next", "next", "."]
    )
    bot.main(read_string=simulate_inputs(inputs), print=output.append)
    assert output[100:] == [
        "John4 4: Phones: 1234567894\n"
        "John4 9: Phones: 1234567894\n"
        "John4 14: Phones: 1234567894\n"
        "John4 19: Phones: 1234567894\n"
        "John4 24: Phones: 1234567894",
        "John4 29: Phones: 1234567894\n"
        "John4 34: Phones: 1234567894\n"
        "John4 39: Phones: 1234567894\n"
        "John4 44: Phones: 1234567894\n"
        "John4 49: Phones: 1234567894",
        "John4 54: Phones: 1234567894\n"
        "John4 59: Phones: 1234567894\n"
        "John4 64: Phones: 1234567894\n"
        "John4 69: Phones: 1234567894\n"
        "John4 74: Phones: 1234567894",
        "John4 79: Phones: 1234567894\n"
        "John4 84: Phones: 1234567894\n"
        "John4 89: Phones: 1234567894\n"
        "John4 94: Phones: 1234567894\n"
        "John4 99: Phones: 1234567894",
        "No more data to scroll",
        "John0 0: Phones: 1234567890\n"
        "John0 5: Phones: 1234567890\n"
        "John0 10: Phones: 1234567890\n"
        "John0 15: Phones: 1234567890\n"
        "John0 20: Phones: 1234567890",
        "John0 25: Phones: 1234567890\n"
        "John0 30: Phones: 1234567890\n"
        "John0 35: Phones: 1234567890\n"
        "John0 40: Phones: 1234567890\n"
        "John0 45: Phones: 1234567890",
        "John0 50: Phones: 1234567890\n"
        "John0 55: Phones: 1234567890\n"
        "John0 60: Phones: 1234567890\n"
        "John0 65: Phones: 1234567890\n"
        "John0 70: Phones: 1234567890",
        "John0 75: Phones: 1234567890\n"
        "John0 80: Phones: 1234567890\n"
        "John0 85: Phones: 1234567890\n"
        "John0 90: Phones: 1234567890\n"
        "John0 95: Phones: 1234567890",
        "No more data to scroll",
    ]


@pytest.mark.freeze_time
def test_delete_birthday(freezer):
    freezer.move_to("2023-05-30")
    output = []
    bot.main(
        read_string=simulate_inputs(
            [
                "add John, 867594568901, 12/10/2009",
                "days to birthday John",
                "delete birthday John",
                "days to birthday John",
            ]
        ),
        print=output.append,
    )
    assert output == [
        "John is added to Contacts",
        "135 days",
        "Birthday is deleted from contact John",
        "Birthday is not defined for John",
    ]


def test_delete_record():
    output = []
    bot.main(
        read_string=simulate_inputs(
            [
                "add John, 867594568901",
                "add Jane, 867594568901",
                "remove John",
                "phone John",
                "remove Mary",
                "phone Jane",
            ]
        ),
        print=output.append,
    )
    assert output == [
        "John is added to Contacts",
        "Jane is added to Contacts",
        "John is removed from Contacts",
        "<Name: John> doesn't exist",
        "<Name: Mary> doesn't exist",
        "867594568901",
    ]


def test_phones():
    output = []
    bot.main(
        read_string=simulate_inputs(
            [
                "add Jane, 867594568901",
                "add phone Jane, 1234567890",
                "add phone Jane, 1234567890",
                "add phone Jane, 1234567890",
                "add phone Jane, 1234567890",
                "add phone Jane, 1234567890",
                "add phone Jane, 1234567890",
                "phones Jane",
                "next",
                "next",
            ]
        ),
        print=output.append,
    )
    assert output == [
        "Jane is added to Contacts",
        "Number 1234567890 is added to contact Jane",
        "Number 1234567890 is added to contact Jane",
        "Number 1234567890 is added to contact Jane",
        "Number 1234567890 is added to contact Jane",
        "Number 1234567890 is added to contact Jane",
        "Number 1234567890 is added to contact Jane",
        "867594568901\n1234567890\n1234567890\n1234567890\n1234567890",
        "1234567890\n1234567890",
        "No more data to scroll",
    ]


def test_search_by_phone():
    output = []
    bot.main(
        read_string=simulate_inputs(
            [
                "add John, 867594568901",
                "add Jane, 867594568901",
                "add phone Jane, 1234567890",
                "search phone 867594568901",
                "search phone 1234567890",
            ]
        ),
        print=output.append,
    )
    assert output == [
        "John is added to Contacts",
        "Jane is added to Contacts",
        "Number 1234567890 is added to contact Jane",
        "John: Phones: 867594568901\nJane: Phones: 867594568901, 1234567890",
        "Jane: Phones: 867594568901, 1234567890",
    ]
