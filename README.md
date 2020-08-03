# Stats Collector

## How it Came to Be
I was asked to help out a colleague who needed visualization of performance and utilization of some Linux machines that did not have any type of CDM monitoring installed.  I did not want to have to install any additional software on the machine, and it seemed like a good opportunity to learn InfluxDB and Grafana.

## What It Does
The main script is a rehash of something I'd done 10+ years ago with `rrdtool`.  This isn't a super deep dive into the health of the machine, but does give a nice overview of what is happening.  Also, the idea is to be able to collect these data without installing any additional software on the machine, such as Python modules.  The bash version will definitely work without any issues, and the python version _should_ work on most recent Linux distributions.

## How To Get it Going
1. Build an AWS Ubuntu instance using the `user-data` file under files.  The size of the instance will likely depend on how much traffic you anticipate.  The script will build out your Influx database, Grafana server and nginx for reverse proxy.
2. When you configure your security groups, make sure that you limit access on port 8086 to those hosts that will be reporting.
3. Go to the IP address of the server, and set the admin password for Grafana.
4. Download the `systemstats.sh` directory to all the machines you want to send data.
5. Set up a `cron` job to run the script every 5 minutes.
6. As the Grafana administrator, you can use the `dashboard.json` file to create pre-set dashboards.  Use `sed` or your favorite text editor and replace "{{ template }}" with the hostname.

## What's Next
This is still very much an "alpha" effort at this point.  I need to get the disk portion in there and cleaned up.  Also, I want to see if I can automate Grafana a little more. Ultimately, I want to get this where you can feed the script a list of hostnames/IP addresses and everything takes care of itself.
