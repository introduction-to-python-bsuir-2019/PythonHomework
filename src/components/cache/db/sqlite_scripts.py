scripts = {
    'write': 'INSERT OR REPLACE INTO {0} ({1}) VALUES ({2});',
    'find_where': 'SELECT id FROM {0} WHERE {1}{2}\'{3}\';',
    'where': 'SELECT * FROM {0} WHERE {1}{2}\'{3}\' LIMIT {4};',
    'get': 'SELECT {1} FROM {0} LIMIT {2};',
    
    'create_db_tables': {
        'feeds': '''
            CREATE TABLE  feeds(
              id       integer PRIMARY KEY autoincrement,
              url      text UNIQUE NOT NULL,
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

              links	         text,
              date           text NOT NULL,
              published  	 timestamp NOT NULL,
              FOREIGN KEY(feed_id) 
                  REFERENCES feeds ( id )
                     ON UPDATE CASCADE
                     ON DELETE CASCADE
            );
            CREATE UNIQUE index unique_feeds_entries_link ON feeds_entries (link);
            ''',
    },

    'load_news': '''
        SELECT fe.* 
        FROM feeds as f 
        JOIN feeds_entries as fe ON f.id = fe.feed_id
        WHERE fe.published >= ? AND fe.published <= ?
        ORDER BY fe.published DESC 
        LIMIT ? 
    '''
}

