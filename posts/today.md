I wanted to start the habit of writing a somewhat daily log of the stuff I do.
To help with that I added a simple alias to my Linux shell. It is called
`today` and does nothing more than to open a textfile named after the
current date in vim.

===ENDPREVIEW===

My to-go shell is [fish](https://fishshell.com). Its pendant to an `rc` dotfile
is located in `~/.config/fish/config.fish`. This file simply contains a fish
script that is run at each start of the shell. Instead of setting an alias I
defined a function called `today`.

    function today
        vim +'norm G' ~/Sync/log/(date +%F).txt
    end

You might spot a few perculiar things:

* `+'norm G'` makes the cursor jump to the bottom of the file. This is useful
for quickly calling the command several times per day.
* The file is stored inside the folder `~/Sync`. I use
[Syncthing](https://syncthing.net) to synchronize the contents of this folder
over all my devices.
* `date +%F` outputs the date in the format `YYYY-MM-DD`. This is a nice level
of verbosity in my opinion.

My aim is to call the function at least once per day and to write about
everything interesting at that point in time. After already a few months of
this I find it fascinating how some useless information from some time ago
feels like a way to look back into the past.
