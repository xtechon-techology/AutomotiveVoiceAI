import random
import datetime
import pyodbc

# Connection to Azure SQL Database
connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:voicepocsqlserver.database.windows.net,1433;Database=voicepocdb;Uid=voicepoc;Pwd=Officenoida@24dec;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Random Data
vehicle_types = [
    "Toyota Camry",
    "Honda Civic",
    "Tesla Model 3",
    "Ford F-150",
    "Chevrolet Bolt",
]
technicians = ["John Doe", "Jane Smith", "Tom Johnson", "Emily Davis"]
customer_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
ratings = [1, 2, 3, 4, 5]

start_date = datetime.date.today() - datetime.timedelta(days=90)
end_date = datetime.date.today()

for _ in range(500):
    service_date = start_date + datetime.timedelta(days=random.randint(0, 89))
    job_number = f"JOB-{random.randint(1000, 9999)}"
    customer_name = random.choice(customer_names)
    vehicle_type = random.choice(vehicle_types)
    parts_cost = round(random.uniform(50, 500), 2)
    labor_cost = round(random.uniform(100, 1000), 2)
    billable_hours = round(random.uniform(1, 8), 2)
    technician_name = random.choice(technicians)
    customer_rating = random.choice(ratings)

    cursor.execute(
        """
        INSERT INTO ServiceJobs (ServiceDate, JobNumber, CustomerName, VehicleType, PartsCost, LaborCost, BillableHours, TechnicianName, CustomerSatisfactionRating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        service_date,
        job_number,
        customer_name,
        vehicle_type,
        parts_cost,
        labor_cost,
        billable_hours,
        technician_name,
        customer_rating,
    )

conn.commit()
cursor.close()
conn.close()
