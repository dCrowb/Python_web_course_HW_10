import json
import psycopg2
import configparser
import pathlib

config = configparser.ConfigParser()
config.read('config.ini')

username = config.get('DB', 'user')
password = config.get('DB', 'password')
db_name = config.get('DB', 'db_name')
host = config.get('DB', 'host')

connection = psycopg2.connect(
    host=host,
    database=db_name,
    user=username,
    password=password
)

cursor = connection.cursor()


def load_data(path):
    with open (path, 'r') as file:
        result = json.load(file)
    return result


def insert_tag(quotes):
    sql_insert = "INSERT INTO quotesapp_tag (name) VALUES (%s)"
    processed_tags = []
    
    for el in quotes:
        for tag in el.get('tags'):
            if not tag in processed_tags:
                processed_tags.append(tag)
                cursor.execute(sql_insert, (tag, ))
                connection.commit()
              
        
def insert_authors(authors):
    sql_insert = "INSERT INTO quotesapp_author (fullname, born_date, born_location, description) VALUES (%s, %s, %s, %s)"
    
    for element in authors:
        fullname = element.get('fullname')
        born_date = element.get('born_date')
        born_location = element.get('born_location')
        description = element.get('description')
        cursor.execute(sql_insert, (fullname, born_date, born_location, description))
        connection.commit()
        
        

def insert_quotes(quotes):
    sql_insert = "INSERT INTO quotesapp_quote (quote, author_id) VALUES (%s, %s)"
    sql_select_id = "SELECT id, fullname FROM quotesapp_author"
    cursor.execute(sql_select_id)
    author_ids = cursor.fetchall()
    
    for el in quotes:
        quote = el.get('quote')
        for author_el in author_ids:
            if el.get('author') in author_el:
                author_id = author_el[0]
        cursor.execute(sql_insert, (quote, author_id))
        connection.commit()
                

def insert_qoute_tags(qoutes):
    insert_tags = "INSERT INTO quotesapp_quote_tags (quote_id, tag_id) VALUES (%s, %s)"
    select_quote_id = "SELECT id FROM quotesapp_quote WHERE quote=%s"
    select_tag_id_tags = "SELECT id FROM quotesapp_tag WHERE name=%s"

    
    for el in qoutes:
        quote = el.get('quote')
        tags = el.get('tags')
        cursor.execute(select_quote_id, (quote,))
        quote_id = cursor.fetchall()
        quote_id = str(quote_id[0]).strip('(').strip(')').strip(',')
        
        for tag in tags:
            cursor.execute(select_tag_id_tags, (tag,))
            tag_id = cursor.fetchall()
            tag_id = str(tag_id[0]).strip('(').strip(')').strip(',')
            cursor.execute(insert_tags, (quote_id, tag_id))
            connection.commit()

        
        
        
        

if __name__ == '__main__':
    authors = load_data('data/authors.json')
    quotes = load_data('data/quotes.json')
    insert_tag(quotes)
    insert_authors(authors)
    insert_quotes(quotes)
    insert_qoute_tags(quotes)