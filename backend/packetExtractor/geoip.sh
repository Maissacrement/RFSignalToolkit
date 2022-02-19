#!/bin/bash
cat /tmp/iplist | xargs -i geoiplookup {} 