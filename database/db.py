
import databases
import sqlalchemy


DATABASE_URL = "postgresql://postgres:77girado@localhost/minzifadb"
engine = sqlalchemy.create_engine(
    DATABASE_URL
)
database = databases.Database(DATABASE_URL)


metadata = sqlalchemy.MetaData()


