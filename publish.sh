#!/bin/sh
rsync -r -a --delete --progress klockenschooster:/var/www/blog.klockenschooster.de/ build
