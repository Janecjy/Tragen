import argparse
import os
import paramiko
import yaml
import math

hosts = []
ssh_hosts = []
config_path = ''
trace_conf_list = []

def connect_rhost(rhost, username):
    rssh = paramiko.client.SSHClient()
    # rssh.load_system_host_keys()
    rssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    rssh.connect(hostname=rhost, username=username)
    s = rssh.get_transport().open_session()
    paramiko.agent.AgentRequestHandler(s)
    rssh.get_transport().set_keepalive(50000)
    return rssh

def setup(host_id):
    rssh_object = ssh_hosts[host_id]

    # setup node
    clone_cmd = "sudo apt-get update; sudo apt-get install -y python3.6 libjpeg-dev zlib1g-dev; sudo apt-get install -y python3-pip; pip3 install numpy scipy PySide2 datetime matplotlib; ssh-keyscan github.com >> ~/.ssh/known_hosts; sudo chown -R janechen /mydata; mkdir -p /mydata/traces; rm -rf Tragen; git clone git@github.com:Janecjy/Tragen.git; cd Tragen; mkdir config"
    stdin, stdout, stderr = rssh_object.exec_command(clone_cmd, get_pty=True)
    for line in iter(stdout.readline, ""):
        print(line)


def copy_conf(host_id, start_conf_num, conf_num):
    for i in range(conf_num):
        # print(start_conf_num+i)
        conf_name = trace_conf_list[start_conf_num+i]
        scp_cmd = "scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "+config_path+"/"+conf_name+" "+username+'@'+hosts[host_id]+":~/Tragen/config/"
        print(scp_cmd)
        os.system(scp_cmd)
    

def run(host_id):
    rssh_object = ssh_hosts[host_id]

    run_cmd = "ls Tragen/config/ | wc -l; cd Tragen; chmod +x scripts/genTrace.sh; tmux new-session -d ./scripts/genTrace.sh"
    print(run_cmd)
    stdin, stdout, stderr = rssh_object.exec_command(run_cmd, get_pty=True)
    for line in iter(stdout.readline, ""):
        print(line)
    for line in iter(stderr.readline, ""):
        print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Offline run simulator experiments')
    parser.add_argument('-f', action="store", dest="config_file_path")
    args = parser.parse_args()
    config_file_path = args.config_file_path
    fp = open(config_file_path, "r")
    yaml_obj = yaml.safe_load(fp)
    hosts = yaml_obj['hosts']
    username = yaml_obj['username']
    config_path = yaml_obj['config_path']
    
    print('total_hosts:', len(hosts))
    trace_conf_list = os.listdir(config_path)
    print('total_confs:', len(trace_conf_list))
    host_conf_num = math.floor(len(trace_conf_list)/len(hosts))
    assigned_conf_num = 0

    for i in range(0, len(hosts)):
        host = hosts[i]
        print(host)
        ssh_object = connect_rhost(host, username)
        ssh_hosts.append(ssh_object)
        setup(i)
        copy_conf(i, assigned_conf_num, host_conf_num)
        assigned_conf_num += host_conf_num

    if assigned_conf_num < len(trace_conf_list):
        copy_conf(i, assigned_conf_num, len(trace_conf_list)-assigned_conf_num)

    for i in range(0, len(hosts)):
        run(i)
