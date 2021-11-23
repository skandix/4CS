# 4CS

## What is 4CS
4CS is a 4chan.org lurker.


## Features
This is still quite work in progress.


### What can it do ?
It provides "simple" features as
* get somewhat okay url that sometime work

### What is Missing ?

* Download all url that is to be found on a 4chan thread or board.
* push all data into elasticsearch db
* Multithreading EVERYTHING + async that shit
* clean up the regex expressions
* SCRAPE ALL BOARDS CONCURRENTLY!
* if a board returns a id instead of a text title, the thread is fucking dead 
* if a thread does not return any content it should be skipped, and not printed out, and then in the end it should give summary of like 2threads with urls matching this word and 69 did not.
* setup github acttions to format code ??

### Usage
```bash
pipenv install; pipenv shell

```