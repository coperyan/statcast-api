from baseball_savant import client, data

bs_client = client.BaseballSavant()
bs_data = data.BaseballSavantData(bs_client, "data")

# Get statcast data, download it
bs_data.fetch_data()

# Get in DF
df = bs_data.get_data_df()
