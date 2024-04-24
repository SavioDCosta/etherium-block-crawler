import requests
import sqlite3
import sys
import datetime

def get_block(block_number, endpoint):
    # Retrieves block data from the Ethereum blockchain via JSON-RPC
    try:
        payload = {
            "method": "eth_getBlockByNumber",
            "params": [hex(block_number), True],  # Request full transaction objects
            "id": 1,
            "jsonrpc": "2.0"
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()  # Will raise an exception for HTTP error codes
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to retrieve block {block_number}: {e}")
        return None

def store_transactions(block_data, cursor):
    # Stores the transaction data from a block into the SQLite database
    try:
        transactions = block_data['result']['transactions']
        hex_timestamp = block_data['result']['timestamp']
        # Convert hexadecimal timestamp to a human-readable datetime format
        timestamp = datetime.datetime.fromtimestamp(int(hex_timestamp, 16), tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        for tx in transactions:
            cursor.execute('INSERT INTO transactions (block_number, `from`, `to`, value, timestamp) VALUES (?, ?, ?, ?, ?)',
                           (str(int(tx['blockNumber'], 16)), tx['from'], tx['to'], str(int(tx['value'], 16)), timestamp))
    except Exception as e:
        print(f"Error storing transactions: {e}")

def query_highest_volume(conn):
    # Queries the database to find the block with the highest volume of Ether transferred within a specified time range
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT block_number, SUM(CAST(value AS REAL)) AS total_volume
            FROM transactions
            WHERE timestamp BETWEEN '2024-01-01 00:00:00' AND '2024-01-01 00:30:00'
            GROUP BY block_number
            ORDER BY total_volume DESC
            LIMIT 1;
        """)
        result = cur.fetchone()
        with open('query_results.txt', 'w') as file:  # Open a file to write the results
            if result:
                file.write(f"Block Number with Highest Volume: {result[0]}\n")
                file.write(f"Total Volume: {result[1]}\n")
            else:
                file.write("No data found for the specified range.\n")
    except Exception as e:
        print(f"Error querying highest volume: {e}")


def setup_database(conn):
    # Sets up the database by dropping the existing table and creating a new one
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS transactions;")
    cur.execute('''
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            block_number INT,
            `from` TEXT,
            `to` TEXT,
            value TEXT,
            timestamp TEXT
        );
    ''')
    conn.commit()

def main():
    # The main function to execute the program
    if len(sys.argv) != 4:
        print("Usage: python block_crawler.py <RPC endpoint> <DB path> <block range>")
        return

    endpoint = sys.argv[1]
    db_path = sys.argv[2]
    block_range = sys.argv[3].split('-')

    if len(block_range) != 2:
        print("Invalid block range. Ensure it is formatted as 'start-end'.")
        return

    start_block, end_block = map(int, block_range)

    try:
        conn = sqlite3.connect(db_path)
        setup_database(conn)  # Prepare the database for fresh data

        for block_number in range(start_block, end_block + 1):
            block_data = get_block(block_number, endpoint)
            if block_data and 'result' in block_data and block_data['result']:
                store_transactions(block_data, conn)
        
        query_highest_volume(conn)  # Execute the query after storing all transactions

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()  # Ensure the database connection is closed

if __name__ == '__main__':
    main()
