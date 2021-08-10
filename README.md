# Baseball Savant

### Data Sources

- Statcast Data from [Baseball Savant](https://baseballsavant.mlb.com/)

### Modules

- Client.py
  - Client to handle auth / requests
- CollectData.py
  - Class Implementation to perform operations on data
  - Performing the request with the client, transforming the data, storing locally
- FetchData.py
  - Module to perform the collect data function with logging

### Dependencies

This package depends on the following packages:

- pandas
- requests

Can install by using `pip`.

`sudo pip install -r requirements.txt`

### Installation

To install, run the following command from the top-level package directory

`sudo python setup.py install`

### Get Started

```
from baseball_savant import client, data

bs_client = client.BaseballSavant()
bs_data = data.BaseballSavantData(bs_client,'data')

#Get statcast data, download it
bs_data.fetch_data()

#Get in DF
df = bs_data.get_data_df()
```

### Reference

-[Pybaseball](https://github.com/jldbc/pybaseball) by James LeDoux
