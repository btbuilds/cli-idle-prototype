from models import Ticket, Customer
from dataclasses import asdict
from storage import load_data, save_data
from constants import COUNTER_FILE

class TicketSystemManager:
    def __init__(self):        
        # Create individual managers
        self.customers = CustomerManager()
        self.tickets = TicketManager()
        self.technicians = TechnicianManager()

class CustomerManager:    
    def create_customer(self, code, name, phone, email, address, is_business):
        customer_dicts = load_data("customers")

        for customer_dict in customer_dicts:
            if customer_dict["code"] == code:
                raise ValueError(f"Customer code {code} already exists.")

        customer = Customer(
            code=code,
            name=name,
            phone=phone,
            email=email,
            address=address,
            is_business=is_business,
            )
        
        customer_dicts.append(asdict(customer))

        save_data("customers", customer_dicts)
    
    def find_by_code(self, code):
        customer_dicts = load_data("customers")
        for customer_dict in customer_dicts:
            if customer_dict["code"] == code:
                return Customer(**customer_dict)
        return None
    
    def get_customer_tickets(self, customer_id):
        ticket_dicts = load_data("tickets")
        customer_tickets = []
        for ticket_dict in ticket_dicts:
            if ticket_dict["customer_id"] == customer_id:
                customer_tickets.append(Ticket(**ticket_dict))
        return customer_tickets

class TicketManager:
    def __init__(self):
        self.ticket_dicts = load_data("tickets")
        
    def create_ticket(self, customer_id, description, equipment_list, created_by):
        # Handle auto-incrementing ticket numbers
        # Create the ticket with proper relationships
        pass
    
    def add_time_entry(self, ticket_id, technician, hours, notes):
        # Time tracking logic
        pass
    
    def calculate_xp_for_completion(self, ticket):
        # Your RPG XP logic
        pass

    def get_next_ticket_number():
        with open(COUNTER_FILE, 'r') as f:
            current_max = int(f.read().strip())
            
        next_number = current_max + 1
        
        with open(COUNTER_FILE, 'w') as f:
            f.write(str(next_number))
        
        return next_number

class TechnicianManager:
    def __init__(self):
        self.technicians_dicts = load_data("technicians")
    
    def login(self, username):
        # Handle technician sessions
        pass
    
    def award_xp(self, tech_id, xp_amount):
        # Update XP and handle leveling up
        pass