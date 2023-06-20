import sqlite3

# Create a connection to the database
conn = sqlite3.connect('parking.db')
conn.execute('PRAGMA foreign_keys = 1')
# Create the parking_lot table
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS parking_lot (parking_lot_id INTEGER PRIMARY KEY AUTOINCREMENT, operating_company_name TEXT NOT NULL, address TEXT NOT NULL, zip TEXT NOT NULL)')

# Create the floor table
cur.execute('CREATE TABLE IF NOT EXISTS floor (floor_id INTEGER PRIMARY KEY AUTOINCREMENT, parking_lot_id INTEGER NOT NULL, floor_number INTEGER NOT NULL, number_of_slots INTEGER NOT NULL, is_floor_full BOOLEAN, FOREIGN KEY (parking_lot_id) REFERENCES parking_lot (parking_lot_id))')

# Create the parking_slot table
cur.execute('CREATE TABLE IF NOT EXISTS parking_slot (parking_slot_id INTEGER PRIMARY KEY AUTOINCREMENT, floor_id INTEGER NOT NULL, slot_number INTEGER NOT NULL, FOREIGN KEY (floor_id) REFERENCES floor (floor_id))')

# Create the parking_slot_reservation table
cur.execute('CREATE TABLE IF NOT EXISTS parking_slot_reservation (parking_slot_reservation_id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER NOT NULL, start_time TIMESTAMP NOT NULL, duration_in_minutes INTEGER NOT NULL, booking_date DATE NOT NULL, parking_slot_id INTEGER NOT NULL, FOREIGN KEY (customer_id) REFERENCES customer (customer_id), FOREIGN KEY (parking_slot_id) REFERENCES parking_slot (parking_slot_id))')

# Create the parking_slip table
cur.execute('CREATE TABLE IF NOT EXISTS parking_slip (parking_slip_id INTEGER PRIMARY KEY AUTOINCREMENT, parking_slot_reservation_id INTEGER NOT NULL, actual_entry_time TIMESTAMP NOT NULL, actual_exit_time TIMESTAMP NOT NULL, duration_parked INTEGER NOT NULL, basic_cost INTEGER NOT NULL, total_cost INTEGER NOT NULL, is_paid BOOLEAN, FOREIGN KEY (parking_slot_reservation_id) REFERENCES parking_slot_reservation (parking_slot_reservation_id))')

# Create the customer table
cur.execute('CREATE TABLE IF NOT EXISTS customer (customer_id INTEGER PRIMARY KEY AUTOINCREMENT, license_number TEXT NOT NULL, registration_date DATE NOT NULL, contact_number TEXT NOT NULL, password TEXT NOT NULL, is_regular BOOLEAN)')

# Create the regular_pass table
cur.execute('''CREATE TABLE IF NOT EXISTS regular_pass (regular_pass_id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER NOT NULL, start_date DATE NOT NULL, cost INTEGER NOT NULL, FOREIGN KEY (customer_id) REFERENCES customer (customer_id))''')

# create an admin table with id and password
cur.execute('CREATE TABLE IF NOT EXISTS admin (admin_id INTEGER PRIMARY KEY AUTOINCREMENT, password TEXT NOT NULL)')

#insert record into parking_lot, parking_slot, floor,regular_pass, admin, customer,regular_pass tables
cur.execute('INSERT INTO parking_lot (operating_company_name, address, zip) VALUES (?, ?, ?)', ('ABC', '123 Main St', '12345'))
cur.execute('INSERT INTO floor (parking_lot_id, floor_number, number_of_slots, is_floor_full) VALUES (?, ?, ?, ?)', (1, 1, 10, False))
cur.execute('INSERT INTO parking_slot (floor_id, slot_number) VALUES (?, ?)', (1, 1))
cur.execute('INSERT INTO parking_slot (floor_id, slot_number) VALUES (?, ?)', (1, 2))
cur.execute('INSERT INTO parking_slot (floor_id, slot_number) VALUES (?, ?)', (1, 3))
cur.execute('INSERT INTO parking_slot (floor_id, slot_number) VALUES (?, ?)', (1, 4))
cur.execute('INSERT INTO parking_slot (floor_id, slot_number) VALUES (?, ?)', (1, 5))
cur.execute('INSERT INTO parking_slot (floor_id, slot_number) VALUES (?, ?)', (1, 6))
cur.execute('INSERT INTO parking_slot (floor_id, slot_number) VALUES (?, ?)', (1, 7))
cur.execute('INSERT INTO parking_slot (floor_id, slot_number) VALUES (?, ?)', (1, 8))
cur.execute('INSERT INTO parking_slot (floor_id, slot_number) VALUES (?, ?)', (1, 9))
cur.execute('INSERT INTO parking_slot (floor_id, slot_number) VALUES (?, ?)', (1, 10))
cur.execute('INSERT INTO customer (license_number, registration_date, contact_number, password, is_regular) VALUES (?, ?, ?, ?, ?)', ('123456789', '2020-01-01', '1234567890', 'password', False))
cur.execute('INSERT INTO regular_pass (customer_id, start_date, cost) VALUES (?, ?, ?)', (1, '2020-01-01', 100))
cur.execute('INSERT INTO admin (password) VALUES (?)', ('password',))

# Commit the changes
conn.commit()

# Close the connection
conn.close()