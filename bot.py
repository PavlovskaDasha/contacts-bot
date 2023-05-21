Contact_book = {}


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError as e:
            return f"{e} doesn't exist"
        except IndexError:
            return f'Not enough data for this command'
        except ValueError as e:
            return f'Please enter a valid {e}'
    return wrapper


def read_string():
    string = input('Please enter your command: ')
    return string


def command_parser(string):
    parsed = string.split(' ')
    command = parsed[0]
    args = parsed[1:]
    return command, args


def hello(args):
    return 'How can I help you?'


@input_error
def add(args):
    name = (' ').join(args[0:-1])
    phone = args[-1]
    if len(phone) < 10:
        raise ValueError(f"phone")
    else:
        Contact_book[name] = phone
        return f'{name} is added to Contacts'


@input_error
def change(args):
    name = (' ').join(args[0:-1])
    phone = args[-1]
    if len(phone) < 10:
        raise ValueError(f"phone")
    else:
        Contact_book[name]
        Contact_book[name] = phone
        return f'Number is changed for {name}'


@input_error
def phone(args):
    i = (' ').join(args)
    return Contact_book[i]


def show_all(args):
    if not Contact_book:
        return 'Contact book is empty'
    else:
        output = []
        for key, value in Contact_book.items():
            output.append(f'{key}: {value}')
        return '\n'.join(output)


Handler = {
    'hello': hello,
    'add': add,
    'change': change,
    'phone': phone,
    'show': show_all
}


def main(read_string=read_string, print=print):
    while True:
        user_input = read_string()
        command, args = command_parser(user_input)

        if command == ".":
            break
        if user_input in ['good bye', 'close', 'exit']:
            print('Good bye!')
            break
        if command not in Handler:
            print("Please rephrase your command")
            continue
        print(Handler[command](args))


if __name__ == '__main__':
    main()
