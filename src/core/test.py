from manager import TicketSystemManager
from storage import initialize_files
from models import Equipment, TicketNote

def main():
    initialize_files()
    manager = TicketSystemManager()
    manager.tickets.create_ticket(customer_id="TEST5", 
                                  ticket_type="INHOUSE", 
                                  description="Issue with accessing server",
                                  equipment_list=[Equipment(eq_type="Desktop",
                                                            model="Optiplex 3080",
                                                            serial_number="12345ABC",
                                                            notes="")],
                                  created_by="BT")
    # Create_customer will give a value error if the customer id already exists
    manager.customers.create_customer(code="TEST7",
                                      name="Test Customer",
                                      phone="555-555-5555",
                                      email="test@example.com",
                                      address="123 Test Rd, Los Angeles CA",
                                      is_business=False)
    manager.tickets.add_time_entry(ticket_id="fad698ff-f26f-4dde-9fe4-5cb971fb190c",
                                   ticket_number=18,
                                   technician="BT",
                                   notes="""Booted to Windows
Got system specs
This CPU upgrade is incredibly minor (ryzen 5 5600x to ryzen 7 5800xt)
Recommend customer return CPU as it will likely be less than 10% difference
Spoke with customer and explained my thoughts, along with other possible upgrades (5700x3d, 5800x3, RAM) that could actually make more of a difference
Customer understood and appreciated me explaining things to him
He will pick up in the morning without doing the upgrade""",
                                    hours=0.25,
                                    mileage=0)

main()