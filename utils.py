#  -*- coding: utf-8 -*-
import logging
import codecs

FORMAT = "[%(asctime)s] : %(filename)s.%(funcName)s():%(lineno)d - %(message)s"
DATEFMT = '%H:%M:%S, %m/%d/%Y'
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt=DATEFMT)
logger = logging.getLogger(__name__)

LEXICONPATH="/shared/experiments/mayhew2/lexicons/"

#!/usr/bin/python
langmap = {
    "eng" : "en",
    "ben" : "bn",
    "hin" : "hi",
    "mal" : "ml",
    "nld" : "nl",
    "rus" : "ru",
    "spa" : "es",
    "tam" : "ta",
    "tgl" : "tl",
    "tur" : "tr",
    "uig" : "ug",
    "urd" : "ur",
    "uzb" : "uz",
    "yor" : "yo",
    "deu" : "de",
    "fra" : "fr"}

def getword(line):
    """ returns the word out of a conll line, or None if no word """
    sline = line.split("\t")
    if len(sline) > 5:
        return sline[5]
    return None

def readconll(fname):
    """ Read lines from a conll file."""
    with codecs.open(fname, "r", "utf-8") as f:
        lines = f.readlines()        
    return lines

def writeconll(outfname, outlines):
    with codecs.open(outfname, "w", "utf-8") as out:
       for line in outlines:
           out.write(line);
    

def readplaintext(fname):
    """ Plaintext refers to a single sentence per line. This returns
    lines in the same format as a conll file, but with no labels."""
    with codecs.open(fname, "r", "utf-8") as f:
        lines = f.readlines()

    outlines = []
    for line in lines:
        outlines.extend(plaintexttolines(line))
        outlines.append("\n")
        
    return outlines

def plaintexttolines(text):
    outlines = []
    words = text.split()
    for w in words:
        if w[-1] in [".", ",", "!", ":", ";", "\""]:
            outlines.append("\t".join(["O", "x", "x", "x", "x", w[:-1], "x", "x", "x"]) + "\n")
            outlines.append("\t".join(["O", "x", "x", "x", "x", w[-1], "x", "x", "x"]) + "\n")
        else:
            outlines.append("\t".join(["O", "x", "x", "x", "x", w, "x", "x", "x"]) + "\n")

    return outlines
   


def writeplaintext(outfname, outlines):
    """ Converts conll style lines to sentences, one per line."""
    
    sent = ""
    sents = []
    for line in outlines:
        word = getword(line)
        if word is None:
            sents.append(sent.strip() + "\n")
            sent = ""
        else:
            if len(word) > 0 and word[-1] in [".", ",", "!", ":", ";", "\""]:                
                sent += word
            else:
                sent += " " + word
            
    if sent is not "":
        sents.append(sent)
    
    with codecs.open(outfname, "w", "utf-8") as out:
       for line in sents:
           out.write(line);


def englishexpand(w):
    ret = []
    if w[-1] == "s":
        ret.append(w[:-1])
    if w.endswith("ed"):
        ret.append(w[:-2])
                
    return ret

def uzbekexpand(w):
    ret = []

    suffixes = ["ning", "lik", "lar", "ish", "dan", "idan", "ini","lari", "ga","ni"]

    hassuffixes = True
    modified = False
    while hassuffixes:
        hassuffixes = False
        for s in suffixes:
            if w.endswith(s):
                modified = True
                w = w[:-len(s)]
                hassuffixes = True
                
    if modified:
        ret.append(w)

    if u"ʻ" in w:
        ret.append(w.replace(u"ʻ", ""))

    return ret


           
