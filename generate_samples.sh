#!/bin/sh

python2 ApiWordlistGen.py -f camel -o samples/verb_noun.txt vN
python2 ApiWordlistGen.py -f camel -o samples/verb_noun_post.txt vNf
python2 ApiWordlistGen.py -f camel -o samples/verb_noun_post_by.txt vNfBb
python2 ApiWordlistGen.py -f camel -o samples/verb_pref_noun.txt vpN
python2 ApiWordlistGen.py -f camel -o samples/verb_pref_noun_by.txt vpNBb
python2 ApiWordlistGen.py -f camel -o samples/verb_pref_noun_post.txt vpNf