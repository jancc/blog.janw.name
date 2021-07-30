#!/bin/sh
rsync -r -a --delete --progress build/ klockenschooster:/var/www/blog.janw.name
