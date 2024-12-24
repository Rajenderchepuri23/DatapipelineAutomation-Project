import mysql.connector
import logging

import pandas as pd

def connect_to_db():
    try:
        connection=mysql.connector.connect(
            host="localhost",
            user='root',
            password='Vedha@2018',
            database='Stockdata'
        )

        logging.info('Database connection successfull')
        return connection
    except mysql.connector.Error as err:
        logging.error(f"database connection failed :{err}")
        return None
    
def create_table():
    connection=connect_to_db()
    if connection:
        try:
            cursor=connection.cursor()
            create_table_query= """
                CREATE TABLE IF NOT EXISTS StockPrices (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    symbol VARCHAR(10) NOT NULL,
                    timestamp DATETIME NOT NULL,
                    open_price FLOAT NOT NULL,
                    high_price FLOAT NOT NULL,
                    low_price FLOAT NOT NULL,
                    close_price FLOAT NOT NULL,
                    volume BIGINT NOT NULL
                );
            """
            cursor.execute(create_table_query)
            connection.commit()
            logging.info("Table stockprices has been created succesfully.")
        except mysql.connector.Error as err:
            logging.error(f"failed to create the table:{err}")
        finally:
            cursor.close()
            connection.close()

def insert_stock_data(symbol,stock_data):
    connection = connect_to_db()
    if connection:
        try:
            cursor=connection.cursor()
            if not isinstance(stock_data, pd.DataFrame):
                raise ValueError("Invalid Data Frame .Expected a  data frame")
            logging.info(f"Data for {symbol}:\n{stock_data.head()}")

        
            for _, row in stock_data.iterrows():
                cursor.execute("""

                INSERT INTO Stockprices(symbol,timestamp,open_price,high_price,low_price,close_price,volume)
                VALUES(%s,%s,%s,%s,%s,%s,%s)
            """,

        
               ( symbol,
                row['Timestamp'],
                row["Open"],
                row["High"],
                row["Low"],
                row['Close'],
                row["Volume"]
                ))
            
            connection.commit()
            logging.info(f"Dta for {symbol} inserted successfully. ")
        except mysql.connector.Error as err:
            logging.error(f"Database error:{err}")
        except Exception as e:
            logging.error(f"An unexpected error occurred:{e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            
            
            