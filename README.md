# Host Manager
This is host manager, written in Python langauge. A `/etc/hosts` scripter. This helps you to ban **distracting** websites 
like `facebook.com`, `p*.com` or `instagram.com`.

## Installation
Here's how you can install it...

First, download it...
```shell
cd ~/username/MyApps
# or any_other_path

git clone https://github.com/bishwas-py/host-manager.git
cd ./host-manager
```

After downloading, copy it to `/bin/` or we can say "Bin it"...
```shell
sudo cp do-host.py /bin/dost
```

Now, use it...
```shell
sudo dost 'www.messenger.com' -b
or
sudo dost 'www.facebook.com' --ban-domain
# give sudo privilege if required
```

Those, distracting sites are now banned.