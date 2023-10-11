#!/bin/bash

ncores=2

seedList="0 1"

parallel -j ${ncores} bash execute.sh {} ::: ${seedList}


