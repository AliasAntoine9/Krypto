import pandas as pd
from sqlalchemy import create_engine

# poseidon <=> The engine
db_uri = "sqlite:///../poseidon.db"
poseidon = create_engine(db_uri, echo=True)
tb_name = "opened_positions"

# Insert Data from Sql into a df
df_positions = pd.read_sql_table(
    table_name=tb_name,
    con=poseidon
)
