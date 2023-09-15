# cron-measurement

Python requirement (>=3.7)

## System resource

### install

```sh
$ echo '
[global]
break-system-packages = true
' > ~/.config/pip/pip.conf

$ pip3 install --user psutil
```

## Omron environment sensor

Data fetcher tool for [Omron environment sensor 2JCIE-BU01](https://www.omron.co.jp/ecb/product-detail?partNumber=2JCIE-BU).

![Omron sensor](https://github.com/amane-uehara/resource/blob/master/omron-env-sensor/omron.png)

### Install

```sh
$ sudo apt install python3-dev
$ sudo apt install python3-pip
$ sudo apt install libglib2.0-dev
$ sudo apt install libboost-python-dev
$ sudo apt install libboost-thread-dev libbluetooth3-dev
$ sudo su root
# pip3 install pybluez
# pip3 install gattlib
```

### Run

```sh
$ sudo su root
# python3 fetch_raw_data.py "C8:B2:44:00:00:00"
{"temperature": 2765, "relative_humidity": 6909, "ambient_light": 78, "barometric_pressure": 1007316, "sound_noise": 5319, "etvoc": 29, "eco2": 594, "absolute_humidity":1728}
```

Command line argument `C8:B2:44:00:00:00` is omron sensor's mac address.

### Data

|description          |example         |physical unit |
|:--------------------|:---------------|:-------------|
|`temperature`        |`2558`          |`25.58 ℃`    |
|`relative_humidity`  |`7256`          |`72.56 %`     |
|`ambient_light`      |`78`            |`78 lx`       |
|`barometric_pressure`|`1007316`       |`1007.316 hPa`|
|`sound_noise`        |`5319`          |`53.19 dB`    |
|`etvoc`              |`29`            |`29 ppb`      |
|`eco2`               |`594`           |`594 ppm`     |
|`absolute_humidity`  |`1728`          |`17.28 %`     |

### Reference

* Omron official reference <https://omronfs.omron.com/ja_JP/ecb/products/pdf/CDSC-016A-web1.pdf>
* Omron official sample script <https://github.com/omron-devhub/2jciebl-bu-ble-raspberrypi>

## Inkbird environment sensor

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
# python3 fetch_raw_data.py "49:23:02:F0:00:00"
{"temperature": 2930, "relative_humidity": 6404}
```

Command line argument `49:23:02:F0:00:00` is inkbird sensor's mac address.

## iCloud

iCloud GPS Fetcher.

### Install

```
$ pip3 install pyicloud
```
