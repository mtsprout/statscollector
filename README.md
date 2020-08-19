# Stats Collector

## How it Came to Be
I was asked to help out a colleague who needed visualization of performance and utilization of some Linux machines that did not have any type of CDM monitoring installed.  I did not want to have to install any additional software on the machine, and it seemed like a good opportunity to learn InfluxDB and Grafana.

## What It Does
The main script is a rehash of something I'd done 10+ years ago with `rrdtool`.  This isn't a super deep dive into the health of the machine, but does give a nice overview of what is happening.  Also, the idea is to be able to collect these data without installing any additional software on the machine, such as Python modules.  The bash version will definitely work without any issues, and the python version _should_ work on most recent Linux distributions.

## How To Get it Going
1. Have a .csv file of hostname and ip address for the machines that will receive the agent.
2. Start `deploy.p` with that files as an input, along with the desired size of the EC2 instance.  (Default is t2.micro.)
3. Go to the IP address of the server, and set the admin password for Grafana.
4. Download the `systemstats.sh` (or `systemstats.py`) script to all the machines you want to send data.
5. Set up a `cron` job to run the script every 5 minutes.
6. As the Grafana administrator, you can use the `dashboard.json` file to create pre-set dashboards.  Use `sed` or your favorite text editor and replace "{{ hostname }}" with the hostname.

## What's Next
* Provision Grafana Dashboards automatically for hostnames
* Deploy script to IPs, and select version based on /etc/redhat-relase
* See if these work on Ubuntu
* Other stuff as it comes along
