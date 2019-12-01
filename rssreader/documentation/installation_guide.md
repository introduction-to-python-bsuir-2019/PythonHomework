# RSS reader
RSS reader is a command-line utility that retrieves the RSS URL and prints the results in a human-readable format.

## Guide
1. Сreate docker container
```bash
docker run -it -p 8080:8080 -v /var/run/docker.sock:/var/run/docker.sock python /bin/bash
```
2. Clone [repository](https://github.com/Spanickroon/PythonHomework)
```bash
git clone https://github.com/Spanickroon/PythonHomework.git && cd PythonHomework && git branch --track FinalTask remotes/origin/FinalTask && git checkout FinalTask && ls
```
3. Run the docker and docker-compose installation script. If you get an error, then you have problems with the Internet. Restart the command again
```bash
chmod +x install.sh && . install.sh
```
4. To start the application write
```bash
docker rm my_app |& docker-compose run --name my_app app python -m rssreader
```
Example:
```bash
docker rm my_app |& docker-compose run --name my_app app python -m rssreader "https://news.yahoo.com/rss" --limit 1
```
5. If you want to test the code, see **manual**
6. If you go get the file pdf or html, see **manual**
7. All is ready. Read **manual**.