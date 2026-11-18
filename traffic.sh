#!/usr/bin/env bash
# Setup

# hostnames obscured for the publishing of this tool
# change the variables below before running
# traffic_host=subdomain.example.com

perform_ssh_config() {
  # Add ssh config
  if grep -e "Match host $traffic_host" ~/.ssh/config; then
    echo "[ssh] SSH config already setup"
    sleep 1
    run_script
  else
    echo "[ssh] Configuring SSH config"
    sleep 1
    echo "[ssh] Writing the short-lived certificate to your ssh config file"
    sleep 1
    printf '

#Cloudflared short-lived-cert
Match host ${traffic_host} exec "cloudflared access ssh-gen --hostname %%h"
  Hostname ${traffic_host}
  ProxyCommand cloudflared access ssh --hostname %%h
  IdentityFile ~/.cloudflared/%%h-cf_key
  CertificateFile ~/.cloudflared/%%h-cf_key-cert.pub'>>~/.ssh/config
  echo "[ssh] short-lived-cert written to config file"
  sleep 2
  echo "[ssh] starting the secure shell connection"
  sleep 1
  echo "[ssh] Add your fingerprint, then exit to rerun the script"
  echo "[Access Requested] if required, please select Approve in the browser window"
  sleep 1
  echo "If you see the prompt 'Are you sure you want to continue connecting (yes/no/[fingerprint])?'"
  echo "enter 'yes'"
  echo "then enter 'exit'"
  sleep 1
	ssh root@$traffic_host
  fi
}

# Run
run_script(){
	ssh root@$traffic_host 'cd traffic-generator;
	sleep 1;
	echo "Enter your domain:"; 
	read domain; 
	echo "Do you yave subdomains? y/n"; 
	read subdomains; 
	if [ $subdomains == "y" ]; then
		echo "list them separated with a comma like so: 'foo,bar,etc'"
		read subdomain_list
		echo "python ddos_simulator.py -d $domain -s $subdomain_list"; 
		python ddos_simulator.py  -d $domain -s $subdomain_list
	fi;
	if [ $subdomains == "n" ]; then
		echo "python ddos_simulator.py -d $domain"; 
		python ddos_simulator.py  -d $domain
	fi'
}

perform_ssh_config


