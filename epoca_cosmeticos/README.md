robotCrawl
==========

Crawler robot attack! Just kidding! It's an experiment with new programming languages and webpages.
This repository was created because of a challenge where i should create a crawler which could get info from webpages.
That got out of control and i just want to improve and improve. And it's fun! It's fun when you get to understand the concepts of some types of softwares that are out there in the woods (internet).

Feel free to give your opinion on my code.

==================================================
TL;DR; Note:
==================================================
To run, simply git clone the repo and start the main.py script
ex: ./main.py

I'm using the following modules:
- re
- datetime
- os
- threading
- urllib2
- gzip
- time
- datetime
- httplib
- socket
- StringIO

If you aren't sure if you have those modules, "pip install" the sh!t out of it!
-> Ubuntu 14.04 runs it by default (Python 2.7.6)

===================================================
How have i build this crawler?
Well, the book is on the... Just kidding (again, never seems to fail)!
I'm separating in 3 levels:
The first level is where i get the file containing all the brands that i'm supose to crawl.
With this file in hand, i can get, now, the level 2.
The second level is where i have all brands' pages and aim for the menu from the page to get to the product page.
The third level is the product page.

This is it!

I'm using two approaches: first, to get the level 2 files, i'm using a synchronous method. Only fetch the file if the last one is downloaded. For the level 3 files, i'm using threads. I'm downloading 10 files at a time. It's too slow if i do it in a synchronous way.

Hope you enjoy it!
