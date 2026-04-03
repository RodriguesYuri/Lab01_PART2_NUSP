import great_expectations as gx

context = gx.get_context()

print("Connecting to Raw layer data...")
file_path = 'data_lake/bronze/yellow_tripdata_2019-03.csv'

validator = context.sources.pandas_default.read_csv(file_path)

print("Applying the 5 Expectations...")
# Expectation 1: The pick-up location ID column cannot have null values
validator.expect_column_values_to_not_be_null(column="PULocationID")

# Expectation 2: The total amount of the ride must be positive and less than 5000 dollars
validator.expect_column_values_to_be_between(column="total_amount", min_value=0, max_value=5000)

# Expectation 3: The passenger count must be between 0 and 10
validator.expect_column_values_to_be_between(column="passenger_count", min_value=0, max_value=10)

# Expectation 4: The payment type must be within a known list (1 to 6)
validator.expect_column_values_to_be_in_set(column="payment_type", value_set=[1, 2, 3, 4, 5, 6])

# Expectation 5: The vendor ID column must exist in the table
validator.expect_column_to_exist(column="VendorID")

print("Generating the HTML report (Data Docs)...")
validator.save_expectation_suite(discard_failed_expectations=False)
context.build_data_docs()

print("Validation completed successfully!")
print("Go to the folder: gx/uncommitted/data_docs/local_site/ and open the index.html file in your browser!")