# For ELK
yum -y install java


# ELK 5.6.4
rpm -ivh https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.4.rpm
rpm -ivh https://artifacts.elastic.co/downloads/logstash/logstash-5.6.4.rpm
rpm -ivh https://artifacts.elastic.co/downloads/kibana/kibana-5.6.4-x86_64.rpm


#####
# ELK 6.x
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
