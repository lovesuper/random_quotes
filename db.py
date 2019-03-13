from sqlalchemy import Text, Integer, Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("postgresql://user:user@localhost/quotes_db")
DBSession = sessionmaker(bind=engine)


class Quote(Base):

    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    parsed_id = Column(String(), nullable=False)

    def jsonify(self):
        return {
            "id": self.parsed_id,
            "text": self.text
        }


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
