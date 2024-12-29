import csv
import webbrowser

class Inventory:
    def __init__(self, file_path):
        self.items = self.load_inventory(file_path)

    def load_inventory(self, file_path):
        inventory = {}
        try:
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:
                        inventory[row[0]] = (int(row[1]), row[2])
        except FileNotFoundError:
            print(f"Error: {file_path} not found.")
        return inventory

    def display_inventory(self):
        print("These are the items in the inventory:")
        for key, value in self.items.items():
            print(f"{key} - ${value[0]}")

    def get_item(self, item_name):
        return self.items.get(item_name, None)


class Wallet:
    def __init__(self, initial_balance=100):
        self.balance = initial_balance

    def add_money(self, amount):
        if self.balance + amount > 10000:
            print(f"Wallet cannot exceed $10000. Current balance: ${self.balance}")
            return 0
        else:
            print(f"${amount} has been added.")
            self.balance += amount
            return amount

    def spend_money(self, amount):
        if amount > self.balance:
            print("Sorry, you don't have enough money in your wallet.")
            return 0
        self.balance -= amount
        return amount

    def display_balance(self):
        print(f"You have ${self.balance} in your wallet.")


class User:
    def __init__(self):
        self.bought_items = {}

    def add_item(self, item_name):
        if item_name in self.bought_items:
            self.bought_items[item_name] += 1
        else:
            self.bought_items[item_name] = 1
        print("Item bought.")

    def return_item(self, item_name):
        if item_name in self.bought_items:
            if self.bought_items[item_name] == 1:
                del self.bought_items[item_name]
            else:
                self.bought_items[item_name] -= 1
            print("Item has been returned.")
            return True
        print("Item has not been bought.")
        return False

    def display_belongings(self, wallet_balance):
        print(f"You have ${wallet_balance} in your wallet.")
        if not self.bought_items:
            print("No items have been purchased.")
        else:
            print("You have purchased these items:")
            for key, value in self.bought_items.items():
                print(f"{key} - {value}")


class Shop:
    def __init__(self, inventory_file):
        self.inventory = Inventory(inventory_file)
        self.wallet = Wallet()
        self.user = User()
        self.transaction_file = "transactions.csv"
        self.initialize_transaction_file()

    def initialize_transaction_file(self):
        try:
            with open(self.transaction_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Item Name", "Quantity", "Cost"])
        except IOError:
            print("Error: Unable to initialize transaction file.")

    def log_transaction(self, item_name, quantity, cost):
        try:
            with open(self.transaction_file, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([item_name, quantity, cost])
        except IOError:
            print("Error: Unable to write to transaction file.")

    def remove_transaction(self, item_name):
        try:
            rows = []
            with open(self.transaction_file, "r", newline="") as file:
                reader = csv.reader(file)
                header = next(reader)  # Preserve the header row
                rows.append(header)
                for row in reader:
                    if row[0] != item_name:
                        rows.append(row)
            with open(self.transaction_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)
        except IOError:
            print("Error: Unable to update transaction file.")

    def buy_item(self, item_name):
        item = self.inventory.get_item(item_name)
        if not item:
            print("Item does not exist.")
            return

        cost = item[0]
        if self.wallet.spend_money(cost):
            self.user.add_item(item_name)
            self.log_transaction(item_name, 1, cost)

    def return_item(self, item_name):
        item = self.inventory.get_item(item_name)
        if not item:
            print("Item does not exist in inventory.")
            return

        if self.user.return_item(item_name):
            refund = item[0]
            self.wallet.add_money(refund)
            self.remove_transaction(item_name)

    def view_item_on_web(self, item_name):
        item = self.inventory.get_item(item_name)
        if not item:
            print("Item does not exist.")
            return

        link = f"https://www.amazon.com/dp/{item[1]}"
        webbrowser.open(link)

    def main_menu(self):
        print("\n------ Welcome to Amayzeon! ------")

        while True:
            user_input = input("\nWhat would you like to do?\n'buy' or 'return' or 'add' or 'view' or 'belongings' or 'inventory' or 'exit'\n\n").strip()
            if user_input == "exit":
                print("Goodbye!")
                break
            elif user_input == "inventory":
                self.inventory.display_inventory()
            elif user_input == "belongings":
                self.user.display_belongings(self.wallet.balance)
            elif user_input.startswith("add"):
                try:
                    amount = int(user_input.split(" ")[1])
                    self.wallet.add_money(amount)
                except (IndexError, ValueError):
                    print("Invalid input. Use: add <amount>")
            elif user_input.startswith("buy"):
                try:
                    item_name = user_input.split(" ")[1]
                    self.buy_item(item_name)
                except IndexError:
                    print("Invalid input. Use: buy <item_name>")
            elif user_input.startswith("return"):
                try:
                    item_name = user_input.split(" ")[1]
                    self.return_item(item_name)
                except IndexError:
                    print("Invalid input. Use: return <item_name>")
            elif user_input.startswith("view"):
                try:
                    item_name = user_input.split(" ")[1]
                    self.view_item_on_web(item_name)
                except IndexError:
                    print("Invalid input. Use: view <item_name>")
            else:
                print("Invalid command.")


if __name__ == "__main__":
    shop = Shop("items1.csv")
    shop.main_menu()