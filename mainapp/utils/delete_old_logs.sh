#!/bin/bash
find /home/ssenabulyadavid/ip-monitoring-tool/ip-monitoring-tool -name "mainapp_*" -mtime +7 -exec rm {} \;
