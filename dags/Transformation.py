import pandas as pd


def run_transformation():
    data = pd.read_csv(r"/opt/airflow/dags/zipco_transaction.csv")

    # Remove duplicates
    data.drop_duplicates(inplace=True)

    # handling missing values (filling missing numeric values with the mean or median)
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_columns:
        data.fillna({col: data[col].mean()}, inplace=True)

    # Handle missing string values with unknown
    string_columns = data.select_dtypes(include=['object']).columns
    for col in string_columns:
        data.fillna({col: 'unknown'}, inplace=True)

    # Cleaning date column and assigning the right data type
    data['Date'] = pd.to_datetime(data['Date'])

    # Creating fact and dimension tables
    # create the product table
    products = data[['ProductName']].copy(
    ).drop_duplicates().reset_index(drop=True)
    products.index.name = 'ProductID'
    products = products.reset_index()

    # create customer table
    customers = data[['CustomerName', 'CustomerAddress', 'Customer_PhoneNumber',
                      'CustomerEmail']].copy().drop_duplicates().reset_index(drop=True)
    customers.index.name = 'CustomerID'
    customers = customers.reset_index()

    # create staff table
    staff = data[['Staff_Name', 'Staff_Email']].copy(
    ).drop_duplicates().reset_index(drop=True)
    staff.index.name = 'StaffID'
    staff = staff.reset_index()

    # transaction table
    transaction = data.merge(products, on=['ProductName'], how='left') \
        .merge(customers, on=['CustomerName', 'CustomerAddress', 'Customer_PhoneNumber', 'CustomerEmail'], how='left') \
        .merge(staff, on=['Staff_Name', 'Staff_Email'], how='left')

    transaction.index.name = 'TransactionID'

    transaction = transaction.reset_index()[['Date', 'TransactionID', 'StaffID', 'CustomerID', 'ProductID', 'StoreLocation', 'PaymentType', 'PromotionApplied', 'Weather',
                                             'Temperature', 'StaffPerformanceRating', 'CustomerFeedback', 'DeliveryTime_min', 'OrderType', 'DayOfWeek', 'TotalSales', 'UnitPrice']]

    # save data as csv files.
    data.to_csv('clean_data.csv', index=False)
    products.to_csv('product.csv', index=False)
    customers.to_csv('customer.csv', index=False)
    staff.to_csv('staff.csv', index=False)
    transaction.to_csv('transaction.csv', index=False)

    print('Data cleaning and transformation completed successfully')


if __name__ == "__main__":
    run_transformation()
