# Ethereum Block Crawler and Analyzer

This Python script retrieves Ethereum Mainnet transactions within a given block range and persists them to a SQLite database. It then queries this database to determine which block had the highest volume of ether transferred within a specific time window.

## Prerequisites

To run this script, you'll need:

- **Python 3.x**: Make sure Python 3 is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
- **pip**: Ensure that pip is installed for managing Python packages.
- **Required Python packages**: The script uses `requests` for making HTTP requests and `sqlite3` which is included with Python for database operations.

### Python Packages Installation

Run the following command to install the necessary package:

```bash
pip install requests
```

## Setup

**1. Clone the repository:**
If this script is hosted on a version control system like GitHub, provide cloning instructions. Otherwise, ensure the script and accompanying files are saved locally.
**2. Database Setup:**
The script uses SQLite, which does not require initial setup for the database beyond ensuring the script has permission to write to the directory where the database file (db.sqlite3) will be located.
**G3. et an Ethereum JSON-RPC Endpoint:**
You will need access to an Ethereum JSON-RPC endpoint. Services like Infura or Alchemy provide free access to an endpoint if you sign up with them. Follow their setup guide to get an endpoint URL.

## Configuration

Ensure you have the JSON-RPC endpoint URL ready and determine the block range you are interested in querying.

## Running the Script

To run the script, use the command line. Here is how you can execute the script:

```bash
python block_crawler.py <RPC endpoint> <DB path> <block range>
```

**<RPC endpoint>:** Your Ethereum JSON-RPC endpoint URL.
**<DB path>:** Path to your SQLite database file, e.g., ./transactions.db.
**<block range>:++ The range of blocks to fetch, formatted as start-end, e.g., 18908800-18909050.

## Output

The script will output the results to a file named query_results.txt in the same directory where the script is run. This file will contain the block number and total volume of the block with the highest transaction volume within the specified timestamp range.

## Error Handling

The script includes basic error handling for common issues such as network errors, database errors, and data processing errors. Ensure the console is monitored for any error messages.
