# RSS reader

RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format.


## Specification
Utility provides the following interface:
  + positional arguments:
    + source - RSS URL
  + optional arguments:
    + -h, --help - Show help message and exit.
    + --version  - Print version info.
    + --json     - Print result as JSON in stdout.
    + --verbose  - Outputs verbose status messages.
    + --limit    - Limit news topics if this parameter is provided.
    + --date     - Return cached news from the specified day. Format is %Y%M%D.

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

## Install RSS reader v4.0 (demo, not working)
1. Create docker container:
    ```
    docker run -it -p 8080:8080 -v /var/run/docker.sock:/var/run/docker.sock python /bin/bash
    ```
2. Install docker in container:
    ```
    apt-get update && \
    apt-get -y install apt-transport-https \
         ca-certificates \
         curl \
         gnupg2 \
         software-properties-common && \
    curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg > /tmp/dkey; apt-key add /tmp/dkey && \
    add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
       $(lsb_release -cs) \
       stable" && \
    apt-get update && \
    apt-get -y install docker-ce
    ```
3. Install docker-compose in container:
    ```
    sudo curl -L https://github.com/docker/compose/releases/download/1.24.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    ```
4. Clone or Download repository https://github.com/ZayJob/PythonHomework
5. Go to folder /PythonHomework
6. **git branch**
7. There is no branch besides **master**? Then follow this tutorial:
    ```
    git branch --track finalTask remotes/origin/finalTask
    git checkout finalTask
    ```
8. I recommend creating a virtual environment. **python3.8 -m venv env**, **. env/bin/activate**.
9. Let's collect our package **python3.8 setup.py sdist**.
10. Let's install our package **pip3.8 install dist/rss_reader_ft-4.0.tar.gz**
11. Up MongoDB and Mongo-Express:
    ```
    docker-compose up --build -d
    ```
12. Use:
    ```
    rss-reader "https://news.yahoo.com/rss/" --limit 1
    ```

## Distribution
Utility is wrapped into package named rss_reader_ft. Additionally this package exports CLI utility named rss-reader.

## Caching
The RSS news are stored in a local storage while reading.
