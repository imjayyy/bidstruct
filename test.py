# import pymongo

# import pandas as pd
# from pymongo import MongoClient


# # ['EHB_Auto']['LeadsAPI']



# # Function to check duplicates in CSV file
# def check_csv_duplicates(csv_file_path):
#     df = pd.read_csv(csv_file_path)
#     duplicates = df[df.duplicated()]
#     return duplicates

# def check_duplicates(csv_file_path, mongo_uri, db_name, collection_name, phone_number_field):
#     # Read CSV file
#     csv_df = pd.read_csv(csv_file_path)
#     csv_phone_numbers = set(csv_df[phone_number_field])

#     # Connect to MongoDB
#     client = MongoClient(mongo_uri)
#     db = client[db_name]
#     collection = db[collection_name]

#     # Fetch phone numbers from MongoDB
#     mongo_phone_numbers = set(collection.distinct(phone_number_field))

#     # Find common phone numbers
#     common_phone_numbers = csv_phone_numbers.intersection(mongo_phone_numbers)

#     # Display results
#     print("Phone numbers present in both CSV and MongoDB:")
#     print(common_phone_numbers)

#     # Close MongoDB connection
#     client.close()

# # Example usage
# csv_file_path = "C:/Users/Mujtaba/Desktop/Diabnew-new 13Dec (1).csv"
# mongo_uri = "mongodb+srv://mujtaba:iamdeveloper@cluster0-vzz7w.mongodb.net/%3Cdbname%3E?retryWrites=true&w=majority"
# db_name = "EHB_Auto"
# collection_name = "LeadsAPI"

# phone_number_field = "phone_number"  # Change this to the actual field name in your MongoDB collection

# check_duplicates(csv_file_path, mongo_uri, db_name, collection_name, phone_number_field)



import pandas as pd

# Function to check for duplicates based on phone number in two CSV files
def check_csv_duplicates(csv_file_path1, csv_file_path2, phone_number_field):
    # Read the first CSV file
    csv_df1 = pd.read_csv(csv_file_path1)
    csv_phone_numbers1 = set(csv_df1[phone_number_field])

    # Read the second CSV file
    csv_df2 = pd.read_csv(csv_file_path2)
    csv_phone_numbers2 = set(csv_df2[phone_number_field])

    # Find common phone numbers
    common_phone_numbers = csv_phone_numbers1.intersection(csv_phone_numbers2)

    # Display results
    print("Phone numbers present in both CSV files:")
    print(common_phone_numbers)

# Example usage
csv_file_path1 = "C:/Users/Mujtaba/Desktop/Diabnew-new 13Dec (1).csv"
csv_file_path2 = "C:/Users/Mujtaba/Desktop/EHB_Auto.LeadsAPI.csv"
phone_number_field = "phone_number"  # Change this to the actual field name in your CSV files

check_csv_duplicates(csv_file_path1, csv_file_path2, phone_number_field)
