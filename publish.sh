#!/bin/sh
rsync -r -a --delete --progress build/ janw:/var/www/blog.janw.name
