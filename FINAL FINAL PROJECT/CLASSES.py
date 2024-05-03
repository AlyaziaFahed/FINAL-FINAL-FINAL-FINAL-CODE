from ENUMS import ServiceType, EventType
# Base Person class
class Person:
    """class representing person"""
    def __init__(self, ID, name, address, contact):
        self.ID = ID
        self.name = name
        self.address = address
        self.contact = contact

# Employee class inherits from Person
class Employee(Person):
    """class representing employee"""
    def __init__(self, ID, name, address, contact, department, job_title, salary):
        super().__init__(ID, name, address, contact)
        self.department = department
        self.job_title = job_title
        self.salary = salary

    def modify(self, name, department, job_title, salary):
        self.name = name
        self.department = department
        self.job_title = job_title
        self.salary = salary

# Client class inherits from Person
class Client(Person):
    """class representing client"""
    def __init__(self, client_id, name, address, contact, budget):
        super().__init__(client_id, name, address, contact)
        self.budget = budget
        self.events = []  # This will store EventType instances

    def add_event(self, event):
        self.events.append(event)

    def remove_event(self, event_id):
        self.events = [event for event in self.events if event.event_id != event_id]

    def display_details(self):
        print(f"Client ID: {self.ID}, Name: {self.name}, Budget: {self.budget}")
        for event in self.events:
            print(f"Event Type: {event.name}")


class Service:
    """class representing service"""
    def __init__(self, service_id, name, contact_details, address):
        self.service_id = service_id
        self.name = name
        self.contact_details = contact_details
        self.address = address



class Catering(Service):
    """class representing catering"""
    def __init__(self, service_id, name, contact_details, address, menu, min_guests, max_guests):
        super().__init__(service_id, name, contact_details, address)
        self.menu = menu
        self.min_guests = min_guests
        self.max_guests = max_guests
        self.supplier= None

class Supplier:
    """class representing supplier"""
    def __init__(self, supplier_id, name, address, contact_details, event_type, min_guests, max_guests):
        self.supplier_id = supplier_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.event_type = event_type
        self.min_guests = min_guests if min_guests is not None else 0
        self.max_guests = max_guests if max_guests is not None else 0


class Guest:
    """class representing guest"""
    def __init__(self, guest_id, name, address, contact_details, event_type=None, services=None):
        self.guest_id = guest_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.event_type = event_type
        self.services = services or []

    def calculate_cost(self):
        base_prices = {
            "Wedding": 1000,
            "Birthday": 500,
            "Themed Party": 750,
            "Graduation": 600
        }
        cost = base_prices.get(self.event_type, 0)
        for service in self.services:
            if service == "Catering":
                cost += 200
            elif service == "Cleaning":
                cost += 100
            elif service == "Decorations":
                cost += 150


class Event:
    """class representing event"""
    def __init__(self, event_id, event_type, date, client, venue, guest_list=None, services=None):
        self.event_id = event_id
        self.event_type = event_type  # Should be an instance of EventType enum
        self.date = date
        self.client = client  # This should be an instance of Client
        self.venue = venue  # This should be an instance of Venue
        self.guest_list = guest_list if guest_list is not None else []
        self.services = services if services is not None else []  # List of Service instances
        self.venue.add_event(self)  # Add this event to the venue's schedule


class Venue:
    """class representing venue"""
    def __init__(self, venue_id, name, address, contact, min_guests, max_guests):
        self.venue_id = venue_id
        self.name = name
        self.address = address
        self.contact = contact
        self.min_guests = min_guests
        self.max_guests = max_guests


    def add_event(self, event):
        self.events.append(event) #adds event

    def remove_event(self, event_id): #removes event enum
        self.events = [event for event in self.events if event.event_id != event_id]

    def display_venue_details(self):
        print(f"Venue ID: {self.venue_id}, Name: {self.name}, Address: {self.address}")
        print("Scheduled Events:")
        for event in self.events:
            print(f"- {event.event_id}: {event.event_type.name} on {event.date}")