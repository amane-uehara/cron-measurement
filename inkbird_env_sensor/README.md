### Sensor

Data fetcher tool for [Inkbird environment sensor IBS-TH2](https://inkbird.com/products/hygrometer-ibs-th2).

### Install

```
$ sudo apt-get update
$ sudo apt-get -y upgrade
$ sudo apt-get -y install python3-pip libglib2.0-dev
$ sudo su root
# pip3 install bluepy
```

### Run

```sh
$ sudo su root
# python3 fetch_raw_data.py "49:23:02:00:00:00"
{"temperature": 2930, "relative_humidity": 6404}
```

Command line argument `49:23:02:00:00:00` is inkbird sensor's mac address.
