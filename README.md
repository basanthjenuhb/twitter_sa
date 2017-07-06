# twitter_sa
Integrating twitter SA with with kafka backend

## Install Python3 Dependencies
```bash
pip -r Requirements.txt
```

## Other Dependencies
* Install ElasticSearch
* Install Grafana

## How to run ?

1. Clone the directory
```bash
git clone https://github.com/basanthjenuhb/twitter_sa.git
``` 
  - The google.bin.gz is present in the server. I could not put it to github since its size is 1.5 GB
  - Put that file in resources/ folder
2. Start Kafka Server
  - Login to the user where kafka is installed
```bash
nohup ~/kafka/bin/kafka-server-start.sh ~/kafka/config/server.properties > ~/kafka/kafka.log 2>&1 &
```
3. Start Elastic search
  - Use code in elasticsearch.txt to initialize elasticsearch index
```bash
cd path/to/elasticsearch/directory
bin/elasticsearch -d
```
4. Start sm_client(Twitter client)
  - sm_client takes 3 arguments.
    - Path to twitter configuration file
    - Path to kafka configuration file
    - topic of interest. Ex. modi
```bash
cd twitter_sa/sm_client
java -jar sm_client.jar resources/twitterConfigurations.properties resources/kafkaConfigurations.properties modi
```
5. Start Python consumer
```bash
cd twitter_sa/
python -m consumer.Consumer
```
6. Start grafana
```bash
sudo service grafana-server start
```
  - If grafana is running on a server, you can do ssh tunneling to view it on ur local system
```bash
ssh -N -f -L localhost:3000:localhost:3000 user@remote_host
```
  - Go to your browser and type [localhost:3000](http://localhost/3000 "localhost:3000")
  - username: basanthjenuhb@gmail.com
  - password: 12345
  - Go to twitter feed dashboard to see results
