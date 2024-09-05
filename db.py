from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    year = Column(Integer)
    cv_id = Column(String)
    cv_path = Column(String)
    cv_loaded = Column(Boolean)
    hs_id = Column(String)
    hs_path = Column(String)
    hs_loaded = Column(Boolean)
    complete = Column(Boolean)

class Db():

    def __init__(self, db_path):
        self.engine = create_engine(f'sqlite:///{db_path}')  
        
        Session = sessionmaker(bind=self.engine)
        self.session =   Session()
    
    def create_db(self):
        Base.metadata.create_all(self.engine)


    def load_users(self, user_list_path):
        users = pd.read_csv(user_list_path)
        users.to_sql('user', self.engine, if_exists='append', index=False)

    def get_users(self):
        
        return self.session.query(User).all()
    
    def commit(self):
        self.session.commit()