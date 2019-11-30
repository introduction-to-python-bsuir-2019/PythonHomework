# RSS reader

RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format.


## Specification

**Is used Docker + docker-compose**

Utility provides the following interface:
  + positional arguments:
    + source - RSS URL
  + optional arguments:
    + -h, --help - Show help message and exit.
    + --version  - Print version info.
    + --json     - Print result as JSON in stdout.
    + --verbose  - Outputs verbose status messages.
    + --limit    - Limit news topics if this parameter is provided.
    + --date     - Return cached news from the specified day. Format is %Y%M%D. Shows the news of the day when you viewed them
    + --to-html  - Print result as in HTML file
    + --to-pdf   - Print result as in PDF file

## Install RSS reader v2.0 (work)
1. Create docker container:
    ```
    docker run -it python /bin/bash
    ```
2. Clone or Download repository https://github.com/ZayJob/PythonHomework
3. Go to folder /PythonHomework
4. **git branch**
5. There is no branch besides **master**? Then follow this tutorial:
    ```
    git branch --track finalTask remotes/origin/finalTask
    git checkout finalTask
    git checkout cfbdb81
    ```
  
6. I recommend creating a virtual environment. **python3.8 -m venv env**, **. env/bin/activate**.
7. Let's collect our package **python3.8 setup.py sdist**.
8. Let's install our package **pip3.8 install dist/rss_reader_ft-2.0.tar.gz**
9. Let's install req. **pip3.8 install -r requirements.txt**.
10. Use:
    ```
    rss-reader "https://news.yahoo.com/rss/" --limit 1
    ```

## Install RSS reader v5.0 (work)
1. Create docker container:
    ```
    docker run -it -p 8080:8080 -v /var/run/docker.sock:/var/run/docker.sock python /bin/bash
    ```
2. Input command:

    ```
    chmod +x install.sh && . install.sh
    ```

3. Use for run app:
    ```
    docker-compose run app python -m rss_reader_ft "https://news.yahoo.com/rss" --limit 2 --json
    ```
4. If you want to see the database, then open a browser and paste the URL ( http://localhost:8081/db/News_feed/feeds )

5. If you want to get and view the HTML or PDF file, execute the following commands:
    ```
        docker ps -a
    ```
    You will see the following:
    ```
    CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS                          PORTS                      NAMES
    f2091f9472f4        pythonhomework_app   "python -m rss_reade…"   2 minutes ago       Exited (0) About a minute ago                              pythonhomework_app_run_4b117e008e87
    9036216a4c28        mongo                "docker-entrypoint.s…"   6 minutes ago       Up 6 minutes                    0.0.0.0:27017->27017/tcp   pythonhomework_mongo_1
    4fc0cef77ca2        mongo-express        "tini -- /docker-ent…"   6 minutes ago       Up 6 minutes                    0.0.0.0:8081->8081/tcp     pythonhomework_mongo-express_1
    b6288a095558        python               "/bin/bash"              21 minutes ago      Up 21 minutes                                              interesting_chatterjee

    ```
    Сopy the name of the last running container and paste as in the *example*
    ```
        template: docker export <NAME> > latest.tar
        
        example: docker export pythonhomework_app_run_4b117e008e87 > latest.tar
    ```
    And we get file:
    ```
        tar -xf latest.tar code/News_feed.html
        
    ```
    or
    ```
        
        tar -xf latest.tar code/News_feed.pdf
    ```
    Go to folder /code
## Distribution
Utility is wrapped into package named rss_reader_ft. Additionally this package exports CLI utility named rss-reader.

## Caching
The RSS news are stored in a local storage while reading.

## Format converter
You should implement the conversion of news in at least two of the suggested format: .html, .pdf

## Output colorization
You should add new optional argument --colorize, that will print the result of the utility in colorized mode