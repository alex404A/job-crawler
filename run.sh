#!/bin/sh

rm ./jd.jl && scrapy crawl xing -o jd.jl 2>&1 | tee output.log
