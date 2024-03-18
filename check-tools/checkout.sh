#!/bin/bash

current=$PWD
module load cray-python
python compare.py
cd $current
