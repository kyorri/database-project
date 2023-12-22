import psycopg2
import os
import configparser
from datetime import datetime


def fetch_configuration(log_location):
    config_location = os.path.join(os.path.join(os.path.abspath(os.curdir), 'cfg'), 'config.ini')
    configuration = configparser.ConfigParser()
    configuration.read(config_location)
    print (config_location)
    config = configuration['database']
    with open(log_location, 'a') as f:
        f.write('$> Configuration data for the PostgreSQL server was fetched successfully!\n')
    return config


def close_app(connection, log_location):
    print('You selected option 0 - exit')
    connection.close()
    with open(log_location, 'a') as f:
        f.write('$> Application is closing!\n')


def search_by_id(connection):
    print('You selected option 1 - search tables by ID')
    cursor = connection.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE';
    """)
    tables = [table[0] for table in cursor.fetchall()]
    print("Available tables:", tables)

    table_name = input('Please enter the table name: ').strip()

    if table_name in tables:
        table_id = f"{table_name.replace('_', '').replace('relationship', '')}ID"
        user_input = input(f'Please enter the {table_name}\'s ID: ')

        cursor.execute(f"SELECT * FROM {table_name} WHERE {table_id} = %s;", (user_input,))
        fetched_value = cursor.fetchone()

        if fetched_value is None:
            print(f'No {table_name.replace("_", " ").replace("relationship", "")} with the ID {user_input} was found.')
        else:
            colnames = [desc[0] for desc in cursor.description]
            print(colnames)
            print(fetched_value)
    else:
        print("Table does not exist.")

    cursor.close()


def insert_data(connection):
    print('You selected option 2 - insert data')
    cursor = connection.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE';
    """)
    tables = [table[0] for table in cursor.fetchall()]
    print("Available tables:", tables)

    table_name = input('Please enter the table name: ').strip()

    if table_name in tables:
        cursor.execute(f'SELECT * FROM {table_name};')
        colnames = [desc[0] for desc in cursor.description]
        print("Column names:", colnames)
        
        user_input = []
        for col in colnames:
            user_input.append(input(f'Please enter the {col}: ').strip())

        insert_input = ', '.join(["%s" for _ in user_input])

        insert_query = f'INSERT INTO {table_name} VALUES ({insert_input});'
        cursor.execute(insert_query, user_input)
        connection.commit()
        print("Data inserted successfully.")
    else:
        print("Table does not exist.")


def update_by_id(connection):
    print('You selected option 3 - update tables by ID')
    cursor = connection.cursor()

    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = [table[0] for table in cursor.fetchall()]
    print("Available tables:", tables)

    table_name = input('Please enter the table name: ').strip()

    if table_name in tables:
        table_id = f"{table_name.replace('_', '').replace('relationship', '')}ID"
        user_input_id = input(f'Please enter the {table_name}\'s ID to update: ')

        cursor.execute(f"SELECT * FROM {table_name} WHERE {table_id} = %s;", (user_input_id,))
        fetched_value = cursor.fetchone()

        if fetched_value is None:
            print(f'No {table_name.replace("_", " ").replace("relationship", "")} with the ID {user_input_id} was found.')
        else:
            colnames = [desc[0] for desc in cursor.description]
            print("Column names:", colnames)

            update_col = input(f'Please enter the column to update from {colnames}: ').strip()
            update_value = input(f'Please enter the new value for {update_col}: ').strip()

            update_query = f"UPDATE {table_name} SET {update_col} = %s WHERE {table_id} = %s;"
            cursor.execute(update_query, (update_value, user_input_id))
            connection.commit()
            print("Record updated successfully.")
    else:
        print("Table does not exist.")

    cursor.close()


def delete_by_id(connection):
    print('You selected option 4 - delete record by ID')
    cursor = connection.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE';
    """)
    
    tables = [table[0] for table in cursor.fetchall()]
    print("Available tables:", tables)

    table_name = input('Please enter the table name: ').strip()

    if table_name in tables:
        table_id = f"{table_name.replace('_', '').replace('relationship', '')}ID"
        user_input_id = input(f'Please enter the {table_name}\'s ID to delete: ')

        cursor.execute(f"SELECT * FROM {table_name} WHERE {table_id} = %s;", (user_input_id,))
        fetched_value = cursor.fetchone()

        if fetched_value is None:
            print(f'No {table_name.replace("_", " ").replace("relationship", "")} with the ID {user_input_id} was found.')
        else:
            confirmation = input(f'Are you sure you want to delete the {table_name} record with ID {user_input_id}? (yes/no): ')
            if confirmation.lower() == 'yes':
                delete_query = f"DELETE FROM {table_name} WHERE {table_id} = %s;"
                cursor.execute(delete_query, (user_input_id,))
                connection.commit()
                print("Record deleted successfully.")
            else:
                print("Deletion canceled.")
    else:
        print("Table does not exist.")

    cursor.close()


def print_all_data(connection):
    print('You selected option 5 - print all data in a table')
    cursor = connection.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE';
    """)
    
    tables = [table[0] for table in cursor.fetchall()]
    print("Available tables:", tables)

    table_name = input('Please enter the table name: ').strip()

    if table_name in tables:
        cursor.execute(f"SELECT * FROM {table_name};")
        records = cursor.fetchall()

        colnames = [desc[0] for desc in cursor.description]
        print(colnames)

        if len(records) > 0:
            for record in records:
                print(record)
        else:
            print(f"No data found in {table_name}.")
    else:
        print("Table does not exist.")

    cursor.close()


def search_by_make_or_model(connection):
    print('You selected option 7 - search for a car by make or model')
    cursor = connection.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE';
    """)
    
    tables = [table[0] for table in cursor.fetchall()]

    if 'car' in tables:
        make_or_model = input('Enter the car make or model: ').strip()

        search_query = f"""
            SELECT *
            FROM car
            WHERE 
                Make ILIKE %s OR
                Model ILIKE %s;
        """

        cursor.execute(search_query, (f'%{make_or_model}%', f'%{make_or_model}%'))
        matching_cars = cursor.fetchall()

        if len(matching_cars) > 0:
            print("Matching cars:")
            for car in matching_cars:
                print(car)
        else:
            print("No cars found matching the criteria.")
    else:
        print("Car table does not exist.")

    cursor.close()


def main():
    log_filename = 'log.txt'
    log_dir_path = os.path.join(os.path.abspath(os.curdir), 'logs')
    log_location = os.path.join(log_dir_path, log_filename)
    with open(log_location, 'w') as f:
        f.write(f'[{datetime.now()}]\n')
        f.write('$> Application started!\n')
    config = fetch_configuration(log_location)
    os.system('cls')
    try:
        connection = psycopg2.connect(
            database=config['database'],
            host=config['host'],
            user=config['user'],
            password=config['password'],
            port=config['port']
        )
    except psycopg2.Error as e:
        print("Error:", e)
        with open(log_location, 'a') as f:
            message = ('$> The application could not connect to the database!\n'
                       '$> Please check if the PostgreSQL server is up and running, '
                       'or if the credentials in the configuration file are incorrect.')
            f.write(message)
        return
    finally:
        if (connection):
            with open(log_location, 'a') as f:
                f.write('$> The application successfully connected to the PostgreSQL server!\n')

        # Application main loop
        menu_selection = None
        while menu_selection != '0':
            print('\nWelcome to the car museum database!')
            print('Your options are:')
            print('0 - Close the application')
            print('1 - Search data')
            print('2 - Insert data')
            print('3 - Update data')
            print('4 - Delete data')
            print('5 - Print all data from table')
            print('6 - Search cars by brand and/or make')
            menu_selection = input('Please select an option: ')
            match (menu_selection):
                case '0':
                    close_app(connection, log_location)
                case '1':
                    search_by_id(connection)
                case '2':
                    insert_data(connection)
                case '3':
                    update_by_id(connection)
                case '4':
                    delete_by_id(connection)
                case '5':
                    print_all_data(connection)
                case '6':
                    search_by_make_or_model(connection)
                case _:
                    print('Invalid selection')
            os.system('pause')
            os.system('cls')
        
        
if __name__ == '__main__':
    main()
