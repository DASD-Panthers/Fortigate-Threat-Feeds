Helpful guides to secure your fortigate VPN and threatfeeds:

Moving SSLVPN to a loopback interface:
https://www.reddit.com/r/fortinet/comments/1b2xmj7/move_sslvpn_to_loopback_interface/

https://community.fortinet.com/t5/FortiGate/Technical-Tip-Prevent-TOR-IP-addresses-from-accessing-SSL-VPN/ta-p/269785

Threatfeeds blocking ASN numbers: 
https://www.reddit.com/r/fortinet/comments/1b2ewwo/using_sslvpn_reduce_your_security_footprint_block/


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This python script scrapes the URL's of many common hosting providers and known malicious ASN networks that attackers use for USA based attacks. So even if you are geoblocking everything but the USA for access, you are more than likely still getting attackers attempting to connect to your on-site services.  For an example, before adding this blocklist to my firewall I was seeing roughly 20k attempted connections over the course of 4 days.  After implementing these ASN blocks I cut it down to 0 at the time of writing.  As different ASN's get used for attack I can add them to the master list which will then run daily and be automatically updated into my firewall threatfeed.  While those 20k attempted connections were all failures, straight out blocking them makes sense because you never know when a zero day vulnerability will come out and may give the attacker a way into your network.  

Many attackers rotate their connections across many IP's so blocking individual public IP's can be like whack-a-mole.  If you find the common IP range they are attacking you from you can look up the ASN number and block their whole IP range to prevent futher issues.  

The source of all the data to scrape is the "MasterASN-List.txt" file.  In there you add a name description of the ASN if you want and the URL of the ASN provider.  The URL I like to use is from ipinfo.app - if you use the same base URL and just update the ASN at the end of it you will get all the networks currently allocated to that ASN in the webpage it points to.  Note: Make sure you add # to the beginning of the name description, the python script knows to ignore this value and not try to bring the data into the output file.  

I have the action script set to run at 8am CST everyday via an action .yml file.  I then point my firewall to the raw data version of the output file "SSLVPN-ASN-Blocks.txt" and set it to update daily after my github script runs its update.  There is a similar process I found that does all of this but it is ran locally in a linux server then uploaded to github as part of the script.  I felt doing the entire process in github was a bit easier for most people and removes an additional device on the network to maintain.

How to fix the github workflow error:

1.0 - Change workflow permissions - otherwise it will error out on the actions process.  
1.1 - https://stackoverflow.com/questions/72851548/permission-denied-to-github-actionsbot

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

General setup- if copied:

Note- You can fork off the original if you don't want to maintain your repo. If you want to maintain your own see below.

Download all files from this repo.

Create your repo.

Create your personal access token (follow best practice to expire this after X amount of days.) Copy this code, see details here: https://docs.github.com/en/enterprise-server@3.9/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

Set permissions for token up for Repo, admin:org read, and user.

Open Actions in repo > then click New Workflow > Type "Simple Workflow." Click Configure> name ASN-Scrape.yml as the file name. Copy and paste the .yml code into the edit box that you got for the original repo. This will create .github/workflows folder with .yml file in it.

Go to repo setting > Actions > General > Work flow permissions > select "read and write permissions." 

Next, go to Secrets and Variables> Actions > New Repository secret. Provide whatever name you want, and paste in the personal token code you created earlier. (You will have to rotate this as the personal token expires.)

Finally test by going to Actions > Workflows > Run workflow.

Go to SSLVPN-ASN-Blocks.txt and then click "Raw" to get the URL.

Open FortiGate > Security Fabric > Create New > Threat Feeds > IP address. Paste in the raw GitHub URL. Turn off HTTP basic authentication. Then click OK.

This will create an object on the firewall that can be used for policies to apply however you see fit (ingress/egress.)
