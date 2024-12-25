# DatapipelineAutomation Project

This project automates the fetching, processing, visualization, and storage of stock market data using APIs, Python, and MySQL. It also supports dynamic stock queries and periodic updates via automation.

## Key Features

1. **Automation**:
   - Fetches stock data automatically every 5 minutes for favorite stocks.
   - Logs all activities and errors for easy debugging.

2. **Dynamic Stock Query**:
   - Allows the user to fetch data for any stock dynamically through input.

3. **Data Storage**:
   - Saves stock data into a MySQL database for long-term storage and querying.

4. **Visualization**:
   - Visualizes stock data using line charts for open, high, low, and close prices.

5. **Git Integration**:
   - Project is version-controlled and hosted on GitHub using SSH for secure authentication.

---

## Project Structure

```
DatapipelineAutomation/
├── fetch_data.py     # Main script for fetching, processing, and visualizing stock data.
├── database.py       # Script for database connectivity and data insertion.
├── requirements.txt  # List of Python dependencies.
├── README.md         # Documentation for the project.
```

---

## Technologies Used

- **Programming Language**: Python
- **Database**: MySQL
- **Libraries**:
  - `requests`: Fetch data from the Alpha Vantage API.
  - `pandas`: Process and manipulate data.
  - `matplotlib`: Visualize stock data.
  - `schedule`: Automate periodic tasks.
  - `mysql-connector-python`: Interact with the MySQL database.

---

## Installation and Setup

### Prerequisites

- Python 3.x installed on your system.
- MySQL server installed and running.
- Access to the Alpha Vantage API (API key required).

### Steps

1. Clone the repository:
   ```bash
   git clone git@github.com:Rajenderchepuri23/DatapipelineAutomation-Project.git
   cd DatapipelineAutomation-Project
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the MySQL database:
   - Update `database.py` with your MySQL credentials.
   - Run the `create_table()` function in `database.py` to create the necessary table.

4. Run the automation:
   ```bash
   python fetch_data.py
   ```

---

## Usage

### Dynamic Stock Query
- Run the script and type `fetch` to dynamically fetch data for any stock symbol.

### Automation
- The script automatically fetches data for favorite stocks (`AAPL`, `GOOGL`, `MSFT`, `TSLA`) every 5 minutes.
- Type `wait` to continue automation after manual input.

### Visualization
- After fetching, the script generates a line chart showing the open, high, low, and close prices for the selected stock.

---

## Logging

- Logs are stored in `automation.log`.
- Logs include information about:
  - API responses.
  - Data processing success/failure.
  - Database insertion errors.

---

## Improvements

1. Add support for handling API rate limits.
2. Extend visualization to include more interactive charts.
3. Create a web interface for user interaction.
4. Deploy the project on a cloud platform like AWS or Heroku.

---

## Contribution

Feel free to fork this repository and submit pull requests. For significant changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Author

**Rajender Chepuri**  
GitHub: [Rajenderchepuri23](https://github.com/Rajenderchepuri23)
