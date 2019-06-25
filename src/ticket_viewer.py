import ticket_loader as tl
# from ticket_loader import TicketLoader
# tl = TicketLoader(debug=True)


class State:

    def __init__(self, page_num: int = 1):
        self.code = 'init'
        self.seq = page_num
        self.previous = None

    def get_commands(self):
        if (self.code == 'init'):
            return {'[1] page [x]': 'show page [x] of the ticket list',
                    '[2] exit': 'exit program'}
        elif (self.code == 'page'):
            return {'[1] p': 'previous page',
                    '[2] n': 'next page',
                    '[3] page [x]': 'show page [x] of the ticket list',
                    '[4] ticket [y]': 'show ticket [y] in the current page',
                    '[5] exit': 'exit program'}
        elif (self.code == 'ticket'):
            return {'[1] p': 'previous ticket',
                    '[2] n': 'next ticket',
                    '[3] ticket [y]': 'show ticket [y] in the current page',
                    '[4] back': 'back to ticket list view',
                    '[5] exit': 'exit program'}
        elif (self.code == 'error'):
            return {'[1] back': 'back to previous state',
                    '[2] exit': 'exit program'}
        # elif (self.code == 'repeat'):
        #     return {}
        # elif (self.code == 'end'):
        #     return {}
        else:
            print("ERROR: illegal state code for get_commands")
            return {}

    # check command syntax
    def check_command(self, command: str):
        command = command.strip().lower().split()
        if len(command) == 1:
            if command[0] in ['exit', 'p', 'n', 'back']:
                return command
        elif len(command) == 2:
            if command[0] in ['page', 'ticket']:
                try:
                    command[1] = int(command[1])
                    return command
                except Exception as e:
                    pass
        return False

    def change_state_on(self, command: str):
        # handle boundary cases
        if (self.code == 'end'):
            print("ERROR: should not switch on 'end' state")
            return self

        # normalize the command and check syntax
        command = self.check_command(command)
        if not command:
            # self.code = 'Syntax error in command'
            print("Syntax error in command")
            ns = State()
            ns.code = 'repeat'
            ns.previous = self
            return ns

        # handle common commands
        if (command == ['exit']):
            self.code = 'end'
            return self

        # handle different cases depending on self.code and the command
        if (self.code == 'init'):
            if command[0] == 'page':
                ns = State(command[1])
                ns.code = 'page'
                ns.previous = self
                return ns
        elif (self.code == 'page'):
            if command[0] == 'page':
                ns = State(command[1])
                ns.code = 'page'
                ns.previous = self
                return ns
            if command[0] == 'ticket':
                ns = State(command[1])
                ns.code = 'ticket'
                ns.previous = self
                return ns
            if command[0] == 'p':
                ns = State(self.seq - 1)
                ns.code = self.code
                ns.previous = self
                return ns
            if command[0] == 'n':
                ns = State(self.seq + 1)
                ns.code = self.code
                ns.previous = self
                return ns
        elif (self.code == 'ticket'):
            if command[0] == 'ticket':
                ns = State(command[1])
                ns.code = 'ticket'
                ns.previous = self
                return ns
            if command[0] == 'back':
                ps = self.previous
                while (ps and ps.code != 'page'):
                    ps = ps.previous
                return ps
            if command[0] == 'p':
                ns = State(self.seq - 1)
                ns.code = self.code
                ns.previous = self
                return ns
            if command[0] == 'n':
                ns = State(self.seq + 1)
                ns.code = self.code
                ns.previous = self
                return ns
        elif (self.code == 'error'):
            if command[0] == 'back':
                return self.previous
        # if no command-state patterns are matched, the command is not suitable
        # use a 'repeat' state to indicate this error, handle it in main()
        print("Command '" + command[0] +
              "' should not be used in state " + self.code)
        ns = State()
        ns.code = 'repeat'
        ns.previous = self
        return ns

    # validate the state and present tickets accordingly
    # generate an 'error' state if the current state is not achievable
    def display_state(self):
        print("------ displaying: " + self.code +
              " " + str(self.seq) + " ------")
        if self.code == 'page':
            page = tl.get_page(self.seq)
            if page:
                self.display_page(page)
                return self
            else:
                # ns = State(1)
                # ns.code = 'error'
                # ns.previous = self
                self.code = 'error'
                print("Requested ticket/page is not accessible.")
                return self
        elif self.code == 'ticket':
            # find page_num using pointer to previous state
            ps = self.previous
            while (ps and ps.code != 'page'):
                ps = ps.previous
            ticket = tl.get_ticket(ps.seq, self.seq)
            if ticket:
                self.display_ticket(ticket)
                return self
            else:
                # ns = State(1)
                # ns.code = 'error'
                # ns.previous = self
                self.code = 'error'
                print("Requested ticket/page is not accessible.")
                return self
        elif self.code == 'error':
            print("Requested ticket/page is not accessible.")
        return self

    def display_commands(self):
        if (self.code in ['end', 'repeat']):
            print("ERROR: illegal state code for display_commands")
            return
        else:
            cmds = sorted(self.get_commands().items(), key=lambda x: x[0])
            print("\nPlease enter command of the following formats:")
            for cmd in cmds:
                print("\t" + cmd[0] + ": " + cmd[1])

    def display_page(self, page):
        tickets = page['tickets']
        for i in range(len(tickets)):
            print("#" + str(i+1) + '\t' + self.ticket_summary(tickets[i]))

    def ticket_summary(self, ticket):
        subject = ""
        if 'subject' in ticket:
            subject = ticket['subject']
        tags = None
        if 'tags' in ticket:
            hashtags = ['#' + x for x in ticket['tags']]
            tags = ', '.join(hashtags)
        summary = 'Ticket with subject "' + subject + '"'
        if tags:
            summary += " and tags " + tags
        summary += "."
        return summary

    def display_ticket(self, ticket):
        for key in ticket:
            if ticket[key]:
                print(str(key) + ":\t" + str(ticket[key]))


def main():
    # print welcome message
    tl.print_welcome()

    # initial state
    s = State(1)
    while (s.code != 'end'):
        # print menu for current state
        s.display_commands()
        user_command = input()
        # use user input to update state
        s = s.change_state_on(user_command)
        # discard invalid commands
        if (s.code == 'repeat'):
            s = s.previous
            continue
        # display information (e.g. tickets) according to current state
        s = s.display_state()


if __name__ == "__main__":
    main()


# print state menu
