# For ELK
yum -y install java

ELK_version=5.6.4
ES_host=127.0.0.1
ES_port=9200
K_port=5601
K_host=$(hostname -I)

ES_yml_path="/etc/elasticsearch/elasticsearch.yml"
K_yml_path="/etc/kibana/kibana.yml"


# ELK 5.6.4
rpm -ivh https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-$ELK_version.rpm
rpm -ivh https://artifacts.elastic.co/downloads/logstash/logstash-$ELK_version.rpm
rpm -ivh https://artifacts.elastic.co/downloads/kibana/kibana-$ELK_version-x86_64.rpm


##### ELK 6.x
#cat >/etc/yum.repos.d/elasticsearch.repo <<EOL
#[elasticsearch-6.x]
#name=Elasticsearch repository for 6.x packages
#baseurl=https://artifacts.elastic.co/packages/6.x/yum
#gpgcheck=1
#gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
#enabled=1
#autorefresh=1
#type=rpm-md
#EOL

# yum -y install elasticsearch
# yum -y install logstash
# yum -y install kibana
#####


# Add firewall policies.
firewall-cmd --add-port=$ES_port/tcp --permanent
firewall-cmd --add-port=$K_port/tcp --permanent
firewall-cmd --reload

# YML Settings
sed -i s/'#network.host: 192.168.0.1'/"network.host: $ES_host"/g $ES_yml_path
sed -i s/'#http.port: 9200'/"http.port: $ES_port"/g $ES_yml_path

sed -i s/'#server.port: 5601'/"server.port: $Kport"/g $K_yml_path
sed -i s/'#server.host: "localhost"'/"server.host: $K_host"/g $K_yml_path
sed -i s/"#elasticsearch.url: \"http:\/\/localhost:9200\"/elasticsearch.url: \"http:\/\/$ES_host:$ES_port\""/g $K_yml_path

