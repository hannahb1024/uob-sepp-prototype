import sqlalchemy as sa
#import sqlalchemy.orm
import psycopg2
#from sqlalchemy import 
from sqlalchemy import create_engine

#For encrpyting ${{secrets.POSTGRES_PASSWORD}}?
# import urllib.parse

# urllib.parse.quote_plus("your_${{secrets.POSTGRES_PASSWORD}}")#
def testIDCollect(): #Test IDs for the drop down (returns a list)
    engine = create_engine('postgresql+psycopg2://sepp:${{secrets.POSTGRES_PASSWORD}}@89.241.26.49:5432/marking') #CHANGE THIS TO THE CONTAINER REFERENCE WHEN IT IS READY 

    try:
        with engine.connect() as connection:
            print('Successfully connected to the PostgreSQL database')
            metadata = sa.MetaData()
            testTable = sa.Table('results', metadata, autoload_with=engine, extend_existing=True)
            query = sa.select(testTable.columns.test_id.distinct())
            resultProxy = connection.execute(query)
            resultSet = resultProxy.fetchall()
            return resultSet
        
    except Exception as ex:
        print(f'Sorry failed to connect: {ex}')


def markerDataFromID(id): #Returns all the data from the markers with that test ID

    engine = create_engine('postgresql+psycopg2://sepp:${{secrets.POSTGRES_PASSWORD}}@89.241.26.49:5432/marking') #CHANGE THIS TO THE CONTAINER REFERENCE WHEN IT IS READY

    try:
        with engine.connect() as connection:
            print('Successfully connected to the PostgreSQL database')
            metadata = sa.MetaData()
            markTable = sa.Table('marker', metadata, autoload_with=engine, extend_existing=True)
            query = sa.select(markTable)
            resultProxy = connection.execute(query)
            resultSet = resultProxy.fetchall()
            return resultSet
        
    except Exception as ex:
        print(f'Sorry failed to connect: {ex}')


def testCollect(id): #Test IDs for the drop down (returns a list)

    engine = create_engine('postgresql+psycopg2://sepp:${{secrets.POSTGRES_PASSWORD}}@89.241.26.49:5432/marking') #CHANGE THIS TO THE CONTAINER REFERENCE WHEN IT IS READY

    try:
        with engine.connect() as connection:
            print('Successfully connected to the PostgreSQL database')
            metadata = sa.MetaData()
            testTable = sa.Table('results', metadata, autoload_with=engine, extend_existing=True)
            query = sa.select(testTable).where(testTable.columns.test_id == id)
            resultProxy = connection.execute(query)
            resultSet = resultProxy.fetchall()
            return resultSet

    except Exception as ex:
        print(f'Sorry failed to connect: {ex}')

def updateDatabase(markerID, testID, val): #Updates the database where marker id is the marker id and test id is the test id and val is the values that the mark should change by

    engine = create_engine('postgresql+psycopg2://sepp:${{secrets.POSTGRES_PASSWORD}}@89.241.26.49:5432/marking') #CHANGE THIS TO THE CONTAINER REFERENCE WHEN IT IS READY

    try:
        with engine.connect() as connection:
            print('Successfully connected to the PostgreSQL database')
            metadata = sa.MetaData()
            testTable = sa.Table('results', metadata, autoload_with=engine, extend_existing=True)
            query = sa.select(testTable.columns.result_id, testTable.columns.mark).where(testTable.columns.marker_id == markerID, testTable.columns.test_id == testID)
            resultProxy = connection.execute(query)
            resultSet = resultProxy.fetchall()
            for x in resultSet:
                newMark = x[1] + val
                query = sa.update(testTable).where(testTable.columns.result_id == x[0]).values(mark = newMark) 

    except Exception as ex:
        print(f'Sorry failed to connect: {ex}')




# SQLAlchemy engine

# `engine = create_engine('postgresql+psycopg2://sepp:${{secrets.POSTGRES_PASSWORD}}@127.0.0.1:5432/marking') 


# try:
#     with engine.connect() as connection:
#         print('Successfully connected to the PostgreSQL database')
#         metadata = sa.MetaData()

if __name__ == "__main__":
    test1 = testIDCollect()
    test2 = markerDataFromID(4)
    test3 = testCollect(4)
    test4 = updateDatabase(4, 4, 0)
    print(test1)
    print(test2)
    print(test3)
    print(test4)
# except Exception as ex:
#     print(f'Sorry failed to connect: {ex}')
        # test1 = testIDCollect()
        # test2 = markerDataFromID(4)
        # test3 = testCollect(4)
        # test4 = updateDatabase(4, 4, 0)