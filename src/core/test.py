from manager import TicketSystemManager
from storage import initialize_files
from models import Equipment

def main():
    initialize_files()
    manager = TicketSystemManager()
    manager.tickets.create_ticket(customer_id="TEST4", 
                                  ticket_type="INHOUSE", 
                                  description="Issue with accessing server",
                                  equipment_list=[Equipment(eq_type="Desktop",
                                                            model="Optiplex 3080",
                                                            serial_number="12345ABC",
                                                            notes="")],
                                  created_by="BT")
    # Create_customer will give a value error if the customer id already exists
    manager.customers.create_customer(code="TEST4",
                                      name="Test Customer",
                                      phone="555-555-5555",
                                      email="test@example.com",
                                      address="123 Test Rd, Los Angeles CA",
                                      is_business=False)

main()