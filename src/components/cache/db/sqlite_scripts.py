from src.components.helper import Map


scripts = Map({
    'write': 'INSERT OR REPLACE INTO {0} ({1}) VALUES ({2});',
    'find_where': 'SELECT id FROM {0} WHERE {1} {2} \'{3}\';',
    'where': 'SELECT * FROM {0} WHERE {1} LIMIT {2};',
    'get': 'SELECT {1} FROM {0} LIMIT {2};',

    'create_db_tables': {
        'feeds': '''
            CREATE TABLE  feeds(
              id       integer PRIMARY KEY autoincrement,
              url      text UNIQUE NOT NULL,
              image    text UNIQUE NOT NULL,
              encoding text NOT NULL
            );
            CREATE UNIQUE index unique_feeds_url on feeds (url);
               ''',
        'feeds_entries': '''
            CREATE TABLE feeds_entries (
              id             integer PRIMARY KEY autoincrement,
              feed_id	     integer NOT NULL,
              title	         text NOT NULL,
              description	 text,
              link	         text UNIQUE NOT NULL,
              published  	 timestamp NOT NULL,
              FOREIGN KEY(feed_id) 
                  REFERENCES feeds ( id )
                     ON UPDATE CASCADE
                     ON DELETE CASCADE
            );
            CREATE UNIQUE index unique_feeds_entries_link ON feeds_entries (link);
            ''',
        'feed_entry_links': '''
            CREATE TABLE  feed_entry_links(
              id       integer PRIMARY KEY autoincrement,
              feed_entry_id  integer NOT NULL,
              href     text NOT NULL,
              type     text DEFAULT NULL,
              FOREIGN KEY(feed_entry_id) 
                  REFERENCES feeds_entries ( id )
                     ON UPDATE CASCADE
                     ON DELETE CASCADE
            );
               ''',
        'feed_entry_media': '''
            CREATE TABLE  feed_entry_media(
              id       integer PRIMARY KEY autoincrement,
              feed_entry_id  integer NOT NULL,
              url      text NOT NULL,
              additional text DEFAULT NULL ,
              FOREIGN KEY(feed_entry_id) 
                  REFERENCES feeds_entries ( id )
                     ON UPDATE CASCADE
                     ON DELETE CASCADE
            );
               ''',
    },
})

