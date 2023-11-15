from flask import Flask, request, jsonify, render_template
from datetime import date
import random
import mysql.connector
import requests

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'host': 'mysql', #Change mysql to localhost while deploying and running locally
    'user': 'root',
    'password': 'test1234',
    'database': 'checkout1'
}

@app.route('/insert_user', methods=['GET'])
def insert_user():
    try:
        # Get the data from the request
        data = request.args
        c_name = 'c_two'
        c_mobile = '9898989899'
        c_address = 'ABC Town'
        
        print(c_name,c_mobile,c_address)    #check if data received

        if c_name and c_address and c_mobile:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            insert_query = "INSERT INTO order_checkout (c_name, c_mobile, c_address) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (c_name, c_mobile, c_address))

            connection.commit()
            cursor.close()
            connection.close()
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
    #data = request.args                 # Comment out this code when running in standalone mode
    #user_name = data.get('user_name')   # Comment out this code when running in standalone mode
    #title = data.get('title')           # Comment out this code when running in standalone mode
    #author = data.get('author')         # Comment out this code when running in standalone mode
    #price = data.get('price')           # Comment out this code when running in standalone mode
    user_name = 'testing'    # Delete in final mode
    c1 = user_name[:3]
    c2 = str(random.randint(1000, 9999))
    order_id = c1 + c2  # Generate a random order ID
    
    today = date.today()
    order_date = today.strftime("%d-%b-%Y")

    title = 'Whats a Good Name?'        # Delete in final mode
    author = 'John Roger'              # Delete in final mode
    price = 100.57                      # Delete in final mode

    order_item = title + ' by ' + author
    order_amt = price
    
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Pull data from database
    cursor.execute("SELECT * FROM order_checkout where c_name=%s", (user_name,))
    result = cursor.fetchall()

    for x in result:
        y=x
        user_mobile = "9898989898"
        user_address = "ABS Town"
    
    print(order_id, order_date, order_item, order_amt, user_name, f'Mobile No.{"9898989898"}  Address : {"ABS Town"}')
    
    # Add order data into the order_data table 
    insert_query = "INSERT INTO order_data (order_id, order_date, order_item, order_author, order_cost, order_c_name, order_address, order_mobile) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    print('Order details loaded successfully to order_data table.')
    
    cursor.close()
    connection.close()
    
    return render_template('order_checkout.html', order_id=order_id, order_date=order_date, order_item=order_item, order_amt=order_amt, user_name=user_name, user_address="ABS Town", user_mobile="9898989898")

@app.route('/ret_prod/<user_name>')
def ret_prod(user_name):
    data1 = {'c_name': user_name}
    # Send an HTTP GET request to the Product microservice Customer interface
    response = requests.get('http://localhost:5001/products', params=data1)
    return response.txt


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
