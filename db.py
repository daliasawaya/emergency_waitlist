import os
import re
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

class Database:
    """
    Database class to handle communications between sqlite and the app
    """
    def __init__(self, app) -> None:
        """
        Constructor that creates the database if it does not exists 
        and setups the corresponding functionalities
        """
        __DB_PATH = os.path.join('DB', 'db.sqlite')
        path_exists = os.path.exists(__DB_PATH)
        if not path_exists:
            with open(__DB_PATH, 'w') as file:
                file.write('')
                file.close()
        self.__engine = create_engine(f'sqlite:///{__DB_PATH}')
        self.__session = scoped_session(sessionmaker(autoflush=False, bind=self.__engine))
        sess = self.__session
        if not path_exists:
            self.__reset_db()
        @app.teardown_appcontext
        def destroy_engine(exc=None):
            sess.remove()
        

    def __reset_db(self):
        """
        This method recreates the database with the given
        schema inside the DB/db.schema file
        """
        config_path = os.path.join('DB', 'schema.sql')
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                schmas = re.split(r';\s*$', file.read(), flags=re.MULTILINE)
                for s in schmas:
                    if s:
                        self.__session.execute(text(s))
                file.close()

    def communicate(self, str_txt, params={}):
        """
        A method to execute the sql statement
        """
        ret_val = self.__session.execute(text(str_txt), params)
        return ret_val
    
    def commit(self):
        """
        Commiting the changes to the database
        """
        self.__session.commit()
