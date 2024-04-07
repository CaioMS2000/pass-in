from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.constants import database, database_path

class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = f"{database}:///{database_path}"
        self.__engine = None
        self.__session = None
    
    def connect_to_db(self) -> None:
        self.__engine = create_engine(self.__connection_string)
    
    def get_engine(self):
        return self.__engine
    
    def get_session(self):
        return self.__session
    
    def __enter__(self):
        session_maker = sessionmaker()
        self.__session = session_maker(bind= self.__engine)
        
        return self
        
    def __exit__(self, *args):
        # *args: sua presença é necessária pois apesar de não ser utilizado neste projeto em questão, ainda sim são injetados parâmetros, logo se a função não estiver preparada para recebe-los, é lançado um erro (pelo menos na fase de testes).
        self.__session.close()
        pass
        
db_connection_handler = DBConnectionHandler()