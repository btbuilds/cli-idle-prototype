from models import Ticket, Customer, TicketNote
from typing import Optional
from dataclasses import asdict
from storage import load_data, save_data, initialize_files
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

        customer = Customer(code=code,
                            name=name,
                            phone=phone,
                            email=email,
                            address=address,
                            is_business=is_business)
        
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
    def create_ticket(self, customer_id, ticket_type, description, equipment_list, created_by, contact_name: Optional[str] = "", contact_phone: Optional[str] = ""):
        ticket_dicts = load_data("tickets")
        ticket_number = self.get_next_ticket_number()
        ticket = Ticket(ticket_number=ticket_number, 
                        created_by=created_by, 
                        ticket_type=ticket_type,
                        customer_id=customer_id,
                        description=description,
                        equipment_list=equipment_list,
                        contact_name=contact_name,
                        contact_phone=contact_phone)
        ticket_dicts.append(asdict(ticket))
        save_data("tickets", ticket_dicts)
    
    def add_time_entry(self, ticket_id, ticket_number, technician, notes, hours, mileage):
        ticket_dicts = load_data("tickets")
        ticket_note = TicketNote(ticket_id=ticket_id,
                                 ticket_number=ticket_number,
                                 technician=technician,
                                 notes=notes,
                                 ticket_time=hours,
                                 mileage=mileage)
        ticket = {}
        for ticket_dict in ticket_dicts:
            if ticket_dict["id"] == ticket_id:
                ticket = ticket_dict
                break
        if not ticket:
            raise ValueError(f"Ticket with ID {ticket_id} not found")
        ticket["notes_list"].append(asdict(ticket_note))
        save_data("tickets", ticket_dicts)
    
    def calculate_xp_for_completion(self, ticket):
        # RPG XP logic
        pass

    def get_next_ticket_number(self):
        try:
            with open(COUNTER_FILE, 'r') as f:
                current_max = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            # Fallback or initialize to 0
            current_max = 0
        
        next_number = current_max + 1
        
        with open(COUNTER_FILE, 'w') as f:
            f.write(str(next_number))
        
        return next_number

class TechnicianManager:    
    def login(self, username):
        # Handle technician sessions
        pass
    
    def award_xp(self, tech_id, xp_amount):
        # Update XP and handle leveling up
        pass