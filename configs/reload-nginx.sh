#!/bin/sh
set -eu
/usr/bin/docker exec codyssey-web nginx -t
/usr/bin/docker exec codyssey-web nginx -s reload
