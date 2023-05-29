from inspect import signature, Parameter
import address_book

Handler = {}


class Bot:
    def __init__(self):
        self.contact_book =  address_book.AddressBook()
        self.contact_iterator = None


def input_error(func):
    argument_names = [
        v.name for v in signature(func).parameters.values()
        if v.default == Parameter.empty
    ][1:]
    argument_types = [
        p.annotation for p in signature(func).parameters.values()
    ][1:]
    desc = ", ".join(argument_names)

    def wrapper(bot, *args):
        try:
            if len(args) < len(argument_names):
                return f'Not enough data for this command, please provide: {desc}'
            if len(args) > len(argument_types):
                return f'Too much data for this command, please provide: {desc} (you provided {args})'
            args = [t(a) for (t, a) in zip(argument_types, args)]
            return func(bot, *args)
        except KeyError as e:
            return f"{e} doesn't exist"
        except ValueError as e:
            return f'Please enter a valid {e}'

    Handler[func.__name__.replace('_', " ")] = wrapper
    return wrapper


def read_string():
    string = input('Please enter your command: ')
    return string


def command_parser(cmdline):
    command = ""
    args = []
    for cmd in sorted(Handler.keys(), key=lambda s: len(s), reverse=True):
        if cmdline.startswith(cmd):
            command = cmd
            cmdline = cmdline[len(cmd):].strip()
            break
    if cmdline:
        args = map(str.strip, cmdline.split(','))
    return command, args


@input_error
def hello(bot : Bot):
    return 'How can I help you?'


@input_error
def add(bot : Bot, name: address_book.Name, phone: address_book.Phone, birthday: address_book.Birthday = None):
    bot.contact_book.add_record(address_book.Record(name, phone, birthday))
    return f'{name} is added to Contacts'


@input_error
def add_phone(bot : Bot, name: address_book.Name, phone: address_book.Phone):
    bot.contact_book[name.value].add_phone(phone)
    return f'Number {phone} is added to contact {name}'


@input_error
def delete_phone(bot : Bot, name: address_book.Name, phone: address_book.Phone):
    bot.contact_book[name.value].delete_phone(phone)
    return f'Number {phone} is deleted from contact {name}'


@input_error
def change(bot : Bot, name: address_book.Name, phone: address_book.Phone):
    bot.contact_book.change_phone(name, phone)
    return f'Number is changed for {name}'


@input_error
def phone(bot : Bot, name: address_book.Name):
    return ', '.join(map(str, bot.contact_book[name.value].phones))

@input_error
def set_birthday(bot : Bot, name: address_book.Name, birthday: address_book.Birthday):
    bot.contact_book[name.value].set_birthday(birthday)
    return f'{name} was born on {birthday.value.strftime("%d/%m/%Y")}'

@input_error
def days_to_birthday(bot : Bot, name: address_book.Name):
    return f'{bot.contact_book[name.value].days_to_birthday()} days'

@input_error
def show_all(bot : Bot):
    if not bot.contact_book:
        return 'Contact book is empty'
    else:
        bot.contact_iterator = iter(bot.contact_book)
        return next(bot)

@input_error
def next(bot : Bot):
    if not bot.contact_iterator:
        return "No scrolling context"
    try:
        output = []
        for record in bot.contact_iterator.__next__():
            output.append(f'{record}')
        return '\n'.join(output)
    except StopIteration:
        return "No more data to scroll"


def main(read_string=read_string, print=print):
    bot = Bot()
    while True:
        user_input = read_string()
        command, args = command_parser(user_input)
        if user_input == ".":
            break
        if user_input in ['good bye', 'close', 'exit']:
            print('Good bye!')
            break
        if command not in Handler:
            print("Please rephrase your command")
            continue
        print(Handler[command](bot, *args))


if __name__ == '__main__':
    main()
