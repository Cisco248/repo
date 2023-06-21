import socket
import threading
import time

Host = socket.gethostbyname(socket.gethostname())
Port = 2022

client_data = {}                                                                   # Dictionary to store client ids and their associate data

stock_bids = {'AAPL': {'base_price': 1.32, 'security': 74902, 'profit': 7500},
              'AMZN': {'base_price': 2.45, 'security': 82036, 'profit': 9800},
              'FB': {'base_price': 1.89, 'security': 54028, 'profit': 6700},
              'MSFT': {'base_price': 1.54, 'security': 42103, 'profit': 5900},
              'GOOGL': {'base_price': 2.15, 'security': 96057, 'profit': 8100},
              'TSLA': {'base_price': 3.01, 'security': 25068, 'profit': 10500},
              'YHOO': {'base_price': 1.12, 'security': 73821, 'profit': 4500}}     # Data set of Stocks

client_ids = {}                                                                    # Dictionary to store client IDs

BIDDING_TIME = 60  # seconds
BID_EXTENSION_TIME = 60  # seconds                                                 # Constants for bidding time

def handle_client(client_socket, client_address):                                  # Handle the client connection
    client_socket.send(b"Enter Your ID : ")
    client_id = client_socket.recv(1024).decode().strip()                          # Request the client ID 
    
    if client_id in client_ids :
        client_socket.send(b"ID Already Taken! Disconnecting...")
        client_socket.close()
        return
    
    client_ids[client_id] = client_socket                                          # Add client id to dictionary
    client_socket.close()                                                          # Add  the client_socket
    

    lock = threading.lock()                                                       # Lock =  threading syschoronization
    
    with lock:                                                                     # New  function lock
         if client_id in client_data:
            client_socket.send(b"Id already taken disconnecting")                  # Checking already established
            auction_details = get_auction_details()
            client_socket.send(auction_details.encode())                           # Provide auction details to the client
            
    client_data[client_id] = {'socket' : client_socket, 'socket' : {}}             # Handle the client connection 
     
    while True :
        bid_data = client_socket.recv(1024).decode().strip()                       # Recieve the client bid data
        if not bid_data :
            break
        
        bid_parts = bid_data.split()
        stock_code = bid_parts[0]
        bid_amount = float(bid_parts[1])
        security_code = bid_parts[2]                                               # Parse the bid data
        
        response = process_bid(client_id, stock_code, bid_amount, security_code)   # Process the bid
        client_socket.send(response.encode())                                      # Send the response to the client
    client_socket.close()                                                          # Close the client socket
    
    def process_bid(client_id, stock_code, bid_amount, security_code):                # Check if the stock code is valid
        if stock_code not in stock_bids:
            return f"Invalid Stock Code {stock_code}"

        with lock:                                                                    # Check if the bid is valid
            current_bid = stock_bids[stock_code]['bid']
            current_highest_bidder = stock_bids[stock_code]['bidder']
            current_security_code = stock_bids[stock_code]['security_code']

            if security_code != current_security_code:
                return f"Invalid Security Code {stock_code}"

            if bid_amount <= current_bid:
                return f"Invalid Bid {stock_code} {current_bid}"
            
            if security_code != str(socket[stock_code]['security']) :
                return f"Invalid Security Code {stock_code}"

            stock_bids[stock_code]['bid'] = bid_amount
            stock_bids[stock_code]['bidder'] = client_id                           # Update the highest bid
            client_data[client_id]['stocks'][stock_code] = bid_amount              # Update client's bid for the stock
            track_bid_change(stock_code, client_id, bid_amount)                    # Track the bid change
    
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              # Create a socket object
    server_address = ('', 2022)                                                    # Bind the socket to a specific address and port 
    server_socket.bind(server_address)                                             # Empty string indicates any available network interface
                                                                                   # Listen for incoming connections
    server_socket.listen(5)                                                        # Maximum number of queued connections

    print("Server listening on port 2022")

    while True:
        client_socket, client_address = server_socket.accept()                    # Accept a client connection
        client_thread = threading.Thread(target=handle_client, 
                        args=(client_socket, client_address))                     # Start a new thread to handle the client
        client_thread.start()
start_server()                                                                    # Start the server
        





