from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Database connection
conn = sqlite3.connect('parking.db')
conn.execute('PRAGMA foreign_keys = 1')
cur = conn.cursor()


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Customer registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        license_number = request.form['license_number']
        registration_date = request.form['registration_date']
        contact_number = request.form['contact_number']
        password = request.form['password']
        is_regular = bool(request.form.get('is_regular'))
        conn = sqlite3.connect('parking.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO customer (license_number, registration_date, contact_number, password, is_regular) VALUES (?, ?, ?, ?, ?)',
                    (license_number, registration_date, contact_number, password, is_regular))
        conn.commit()
        return redirect(url_for('home'))
    
    return render_template('register.html')


# Customer login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        license_number = request.form['license_number']
        password = request.form['password']
        conn = sqlite3.connect('parking.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM customer WHERE license_number = ? AND password = ?', (license_number, password))
        customer = cur.fetchone()
        
        if customer:
            session['customer_id'] = customer[0]
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid license number or password')
    
    return render_template('login.html')


# Customer dashboard
@app.route('/dashboard')
def dashboard():
    if 'customer_id' in session:
        customer_id = session['customer_id']
        conn = sqlite3.connect('parking.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM parking_slot_reservation WHERE customer_id = ?', (customer_id,))
        reservations = cur.fetchall()
        
        return render_template('dashboard.html', reservations=reservations)
    else:
        return redirect(url_for('login'))


# Customer reservation
@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if 'customer_id' in session:
        if request.method == 'POST':
            customer_id = session['customer_id']
            start_time = request.form['start_time']
            duration_in_minutes = int(request.form['duration_in_minutes'])
            booking_date = request.form['booking_date']
            parking_slot_id = int(request.form['parking_slot_id'])
            conn = sqlite3.connect('parking.db')
            cur = conn.cursor()
            cur.execute('INSERT INTO parking_slot_reservation (customer_id, start_time, duration_in_minutes, booking_date, parking_slot_id) VALUES (?, ?, ?, ?, ?)',
                        (customer_id, start_time, duration_in_minutes, booking_date, parking_slot_id))
            conn.commit()
            return redirect(url_for('dashboard'))
        conn = sqlite3.connect('parking.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM parking_slot')
        slots = cur.fetchall()
        
        return render_template('reserve.html', slots=slots)
    else:
        return redirect(url_for('login'))


# Customer update reservation
@app.route('/update_reservation/<int:reservation_id>', methods=['GET', 'POST'])
def update_reservation(reservation_id):
    if 'customer_id' in session:
        if request.method == 'POST':
            start_time = request.form['start_time']
            duration_in_minutes = int(request.form['duration_in_minutes'])
            booking_date = request.form['booking_date']
            parking_slot_id = int(request.form['parking_slot_id'])
            conn = sqlite3.connect('parking.db')
            cur = conn.cursor()
            cur.execute('UPDATE parking_slot_reservation SET start_time = ?, duration_in_minutes = ?, booking_date = ?, parking_slot_id = ? WHERE parking_slot_reservation_id = ?',
                        (start_time, duration_in_minutes, booking_date, parking_slot_id, reservation_id))
            conn.commit()
            return redirect(url_for('dashboard'))
        conn = sqlite3.connect('parking.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM parking_slot_reservation WHERE parking_slot_reservation_id = ?', (reservation_id,))
        reservation = cur.fetchone()
        
        cur.execute('SELECT * FROM parking_slot')
        slots = cur.fetchall()
        
        return render_template('update_reservation.html', reservation=reservation, slots=slots)
    else:
        return redirect(url_for('login'))


# Customer delete reservation
@app.route('/delete_reservation/<int:reservation_id>')
def delete_reservation(reservation_id):
    if 'customer_id' in session:
        conn = sqlite3.connect('parking.db')
        cur = conn.cursor()
        cur.execute('DELETE FROM parking_slot_reservation WHERE parking_slot_reservation_id = ?', (reservation_id,))
        conn.commit()
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))


# Admin login
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        password = request.form['password']
        conn = sqlite3.connect('parking.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM admin WHERE password = ? AND admin_id = ?', (password,admin_id))
        admin = cur.fetchone()
        
        if admin:
            session['admin_id'] = admin[0]
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid password')
    
    return render_template('admin_login.html')


# Admin dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' in session:
        conn = sqlite3.connect('parking.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM parking_lot')
        parking_lots = cur.fetchall()
        
        cur.execute('SELECT * FROM floor')
        floors = cur.fetchall()
        
        return render_template('admin_dashboard.html', parking_lots=parking_lots, floors=floors)
    else:
        return redirect(url_for('admin_login'))


# Admin assign parking lot
@app.route('/admin/assign_parking_lot', methods=['GET', 'POST'])
def assign_parking_lot():
    if 'admin_id' in session:
        if request.method == 'POST':
            operating_company_name = request.form['operating_company_name']
            address = request.form['address']
            zip_code = request.form['zip']
            conn = sqlite3.connect('parking.db')
            cur = conn.cursor()
            cur.execute('INSERT INTO parking_lot (operating_company_name, address, zip) VALUES (?, ?, ?)',
                        (operating_company_name, address, zip_code))
            conn.commit()
            return redirect(url_for('admin_dashboard'))
        
        return render_template('assign_parking_lot.html')
    else:
        return redirect(url_for('admin_login'))


# Admin assign floor
@app.route('/admin/assign_floor', methods=['GET', 'POST'])
def assign_floor():
    if 'admin_id' in session:
        if request.method == 'POST':
            parking_lot_id = int(request.form['parking_lot_id'])
            floor_number = int(request.form['floor_number'])
            number_of_slots = int(request.form['number_of_slots'])
            conn = sqlite3.connect('parking.db')
            cur = conn.cursor()
            cur.execute('INSERT INTO floor (parking_lot_id, floor_number, number_of_slots, is_floor_full) VALUES (?, ?, ?, ?)',
                        (parking_lot_id, floor_number, number_of_slots, False))
            conn.commit()
            return redirect(url_for('admin_dashboard'))
        conn=sqlite3.connect('parking.db')
        cur=conn.cursor()
        cur.execute('SELECT * FROM parking_lot')
        parking_lots = cur.fetchall()
        
        return render_template('assign_floor.html', parking_lots=parking_lots)
    else:
        return redirect(url_for('admin_login'))


# Admin assign parking slot
@app.route('/admin/assign_parking_slot', methods=['GET', 'POST'])
def assign_parking_slot():
    if 'admin_id' in session:
        if request.method == 'POST':
            floor_id = int(request.form['floor_id'])
            slot_number = int(request.form['slot_number'])
            conn = sqlite3.connect('parking.db')
            cur = conn.cursor()
            cur.execute('INSERT INTO parking_slot (floor_id, slot_number) VALUES (?, ?)',
                        (floor_id, slot_number))
            conn.commit()
            return redirect(url_for('admin_dashboard'))
        conn = sqlite3.connect('parking.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM floor')
        floors = cur.fetchall()
        
        return render_template('assign_parking_slot.html', floors=floors)
    else:
        return redirect(url_for('admin_login'))

@app.route('/logout')
def logout():
    session.pop('customer_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)