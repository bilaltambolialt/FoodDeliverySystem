# Paste the completed class definitions here.

from abc import ABC, abstractmethod


# 1. User (Abstract Base Class)
class User(ABC):
    def __init__(self, name, phone):
        self._name = name
        self._phone = phone
        self._wallet_balance = 0

    def add_to_wallet(self, amount):
        if amount >= 0:
            self._wallet_balance += amount
            print(f"Wallet balance: ₹{self._wallet_balance}")
        else:
            print("Invalid amount. Cannot add negative money.")

    @abstractmethod
    def notify(self, message):
        pass

    @abstractmethod
    def display_profile(self):
        pass


# 2. Customer
class Customer(User):
    def __init__(self, name, phone, address):
        super().__init__(name, phone)
        self.address = address
        self.order_history = []

    def notify(self, message):
        print(f"Customer Notification ({self._name}): {message}")

    def display_profile(self):
        print("\n--- Customer Profile ---")
        print("Name:", self._name)
        print("Phone:", self._phone)
        print("Wallet:", self._wallet_balance)
        print("Address:", self.address)

    def place_order(self, restaurant, items):
        if not restaurant.is_open():
            print("Restaurant is closed.")
            return None

        menu = restaurant.get_menu()

        for item in items:
            if item not in menu:
                print(f"{item.name} is not available.")
                return None

        order = Order(items)
        bill = order.calculate_bill()

        if self._wallet_balance < bill:
            print("Insufficient wallet balance.")
            return None

        self._wallet_balance -= bill
        self.order_history.append(order)
        self.notify(f"Order {order._order_id} placed successfully.")
        return order


# 3. MenuItem
class MenuItem:
    def __init__(self, name, price, is_veg):
        self.name = name
        self.price = price
        self.is_veg = is_veg

    def __repr__(self):
        food_type = "Veg" if self.is_veg else "Non-Veg"
        return f"{self.name} - ₹{self.price} ({food_type})"


# 4. Restaurant
class Restaurant:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self._menu = []

    def add_item(self, menu_item):
        self._menu.append(menu_item)

    def get_menu(self):
        return self._menu

    def is_open(self):
        return True


# 5. Order
class Order:
    _counter = 1

    def __init__(self, items):
        self._order_id = f"ORD{Order._counter}"
        Order._counter += 1

        self._items = items
        self._status = "Placed"
        self._otp = 1234

    def calculate_bill(self):
        subtotal = sum(item.price for item in self._items)
        gst = subtotal * 0.05
        packaging_fee = 20
        return subtotal + gst + packaging_fee

    def estimated_time(self):
        return 30

    def update_status(self, new_status):
        valid_statuses = ["Placed", "Accepted", "Delivered"]

        if new_status not in valid_statuses:
            print("Invalid order status.")
            return

        self._status = new_status

    def verify_otp(self, otp):
        return str(otp) == str(self._otp)


# 6. DeliveryPartner
class DeliveryPartner(User):
    def __init__(self, name, phone, vehicle):
        super().__init__(name, phone)
        self.vehicle = vehicle
        self.is_available = True
        self.rating = 0.0

    def notify(self, message):
        print(f"Delivery Partner Notification ({self._name}): {message}")

    def display_profile(self):
        print("\n--- Delivery Partner Profile ---")
        print("Name:", self._name)
        print("Phone:", self._phone)
        print("Wallet:", self._wallet_balance)
        print("Vehicle:", self.vehicle)
        print("Available:", self.is_available)
        print("Rating:", self.rating)

    def accept_order(self, order):
        if not self.is_available:
            print("Delivery partner is unavailable.")
            return False

        if order._status != "Placed":
            print("Order cannot be accepted.")
            return False

        order.update_status("Accepted")
        self.is_available = False
        self.notify(f"Accepted order {order._order_id}.")
        return True

    def deliver(self, order, otp):
        if order._status != "Accepted":
            print("Order has not been accepted.")
            return False

        if not order.verify_otp(otp):
            print("Incorrect OTP. Delivery not completed.")
            return False

        order.update_status("Delivered")
        self.is_available = True
        self.notify(f"Order {order._order_id} delivered successfully.")
        return True
