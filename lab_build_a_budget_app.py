"""
Build a simple budget app that tracks spending in different categories
and can show the relative spending percentage on a graph.
"""

import re


class Category:
    def __init__(self, name):
        self.ledger = []
        self.name = name

    def deposit(self, amount, description=""):
        transaction = {"amount": amount, "description": description}
        self.ledger.append(transaction)

    def withdraw(self, amount, description=""):
        transaction = {"amount": -amount, "description": description}

        if self.check_funds(amount):
            self.ledger.append(transaction)

            return True

        return False

    def get_balance(self):
        balance = 0
        for transaction in self.ledger:
            balance += transaction["amount"]

        return balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")

            category.deposit(amount, f"Transfer from {self.name}")
            return True

        return False

    def check_funds(self, amount):
        return True if amount <= self.get_balance() else False

    def turn_int_to_monetary(self, amount):
        amount = round(float(amount), 2)

        amount = str(amount)

        if re.search(r"\.\d\b", amount):
            return amount + "0"

        return amount

    def __str__(self):
        chars_in_name = len(self.name)

        half_asterik_1 = "*" * int((30 - chars_in_name) // 2)
        half_asterisk_2 = "*" * (30 - len(half_asterik_1) - chars_in_name)

        print_head = half_asterik_1 + self.name + half_asterisk_2

        print_body = ""

        for transaction in self.ledger:
            description = transaction.get("description")

            if len(description) > 23:
                description = description[0:23]

            amount = transaction.get("amount")

            amount_monetary = self.turn_int_to_monetary(amount)

            number_count = len(amount_monetary)

            if number_count > 7:
                amount_monetary = amount_monetary[0:7]

            char_count = len(description)
            blank_space = " " * (30 - char_count - number_count)

            print_body += description + blank_space + amount_monetary + "\n"

        total = self.get_balance()
        total = self.turn_int_to_monetary(total)

        return f"{print_head}\n{print_body}Total: {total}"


def create_spend_chart(categories):

    spendings = []
    spending = 0

    spending_histogram = dict()

    for i in categories:

        for transaction in i.ledger:
            if transaction["amount"] < 0:
                spending += abs(transaction["amount"])

        spendings.append(spending)

        spending = 0

    total_spendings = sum(spendings)

    for index, amount in enumerate(spendings):
        percentage = amount / total_spendings * 100

        percent_rounded = 10 * (percentage // 10)

        name = categories[index].name

        spending_histogram[name] = percent_rounded

    print(spending_histogram)

    # Draw the percentages align to the left
    print_graph = ""

    for n in range(100, -10, -10):
        n = str(n)

        blank_space = " " * (4 - 1 - len(n))

        print_percent = blank_space + n + "|" + " "
        print_points = ""

        # Draw the bars represented by 'o'
        for amount in spending_histogram.values():

            if int(n) <= amount:
                print_points += "o  "

            else:
                print_points += "   "

        print_graph += print_percent + print_points + "\n"

    # Print the horizontal line
    print_line = "    " + "---" * len(categories) + "-"

    # Print the category names
    number_of_chars = []
    print_name = ""

    for category in categories:
        name = category.name

        number_of_chars.append(len(name))

    for n in range(max(number_of_chars)):
        print_letters = ""

        for category in categories:
            name = category.name

            try:
                print_letters += name[n] + "  "

            except:
                print_letters += " " + "  "

        print_name += "\n" + " " * 5 + print_letters

    return f"Percentage spent by category\n{print_graph}{print_line}{print_name}"


def main():
    health = Category("Health")
    health.deposit(200, "oftalmo")

    health.withdraw(100)
    health.withdraw(10, "eparema")

    food = Category("Food")

    hygiene = Category("Hygiene")
    hygiene.deposit(80, "deposit")
    hygiene.withdraw(50, "yogurt")
    hygiene.withdraw(10, "pasta")

    health.transfer(10, hygiene)

    print(health)
    print(food)
    print(hygiene)

    categories = (health, food, hygiene)
    print(create_spend_chart(categories))


if __name__ == "__main__":
    main()
