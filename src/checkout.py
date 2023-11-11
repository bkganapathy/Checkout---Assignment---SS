from flask import Flask, request, jsonify, render_template
from datetime import date
import random
import pymysql

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '42519h',
    'database': 'checkout1'
}

@app.route('/insert_user', methods=['GET'])
def insert_user():
    try:
        # Get the data from the request
        data = request.args
        c_name = data.get('c_name')
        c_mobile = data.get('c_mobile')
        c_address = data.get('c_address')
        
        print(c_name,c_mobile,c_address)    #check if data received

        if c_name and c_address and c_mobile:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()

            insert_query = "INSERT INTO order_checkout (c_name, c_mobile, c_address) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (c_name, c_mobile, c_address))

            conn.commit()
            cursor.close()
            conn.close()
            print('Successful')

            return jsonify({'message': 'Order inserted successfully'})
        else:
            print('Error')
            return jsonify({'error': 'Missing data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['POST','GET'])
def process_order():
    print('/process_order:generating order_checkout.html')
    data = request.args
    user_name = data.get('user_name')
    title = data.get('title')
    author = data.get('author')
    price = data.get('price')
    #user_name = 'testing'    # Delete in final mode
    c1 = user_name[:3]
    c2 = str(random.randint(1000, 9999))
    order_id = c1 + c2  # Generate a random order ID
    
    today = date.today()
    order_date = today.strftime("%d-%b-%Y")

    #title = 'Whats a Good Name?'        # Delete in final mode
    #author = 'John Roger'              # Delete in final mode
    #price = 100.57                      # Delete in final mode

    order_item = title + ' by ' + author
    order_amt = price
    
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # Pull data from database
    cursor.execute("SELECT * FROM order_checkout where c_name=%s",(user_name))
    result = cursor.fetchall()

    for x in result:
        y=x
        user_mobile = x[1]
        user_address = x[2]
    print(x)
    print(order_id, order_date, order_item, order_amt, user_name, f'Mobile No.{user_mobile}  Address : {user_address}')
    cursor.close()
    conn.close()
    
    return render_template('order_checkout.html', order_id=order_id, order_date=order_date, order_item=order_item, order_amt=order_amt, user_name=user_name, user_address=user_address, user_mobile=user_mobile)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
