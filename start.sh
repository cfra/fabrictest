#!/bin/sh

ulimit -c unlimited
exec ./start.py "$@"
