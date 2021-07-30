#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 11:44:53 2021

@author: namnguyen
"""
import regex as re
import string


FLAGS = re.MULTILINE | re.DOTALL

def hashtag(text):
    text = text.group()
    hashtag_body = text[1:]
    if hashtag_body.isupper():
        result = " {} ".format(hashtag_body.lower())
    else:
        result = " ".join(["<hashtag>"] + re.split(r"(?=[A-Z])", hashtag_body, flags=FLAGS))
    return result

def allcaps(text):
    text = text.group()
    return text.lower() + " <allcaps>"


def tokenize(text):
    # Different regex parts for smiley faces
    eyes = r"[8:=;]"
    nose = r"['`\-]?"

    # function so code less repetitive
    def re_sub(pattern, repl):
        return re.sub(pattern, repl, text, flags=FLAGS)

    text = re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", "") #url
    #remove username
    #text = re_sub(r"@\w+", "<user>")
    text = re_sub(r"@\w+", " ")
    text = re_sub(r"{}{}[)dD]+|[)dD]+{}{}".format(eyes, nose, nose, eyes), "")
    text = re_sub(r"{}{}p+".format(eyes, nose), "") #lolface
    text = re_sub(r"{}{}\(+|\)+{}{}".format(eyes, nose, nose, eyes), "")
    text = re_sub(r"{}{}[\/|l*]".format(eyes, nose), "")
    text = re_sub(r"/"," / ")
    text = re_sub(r"<3","")
    text = re_sub(r"[-+]?[.\d]*[\d]+[:,.\d]*", "")
    #text = re_sub(r"#\S+", hashtag)
    text = re_sub(r"([!?.]){2,}", r"\1 <repeat>")
    text = re_sub(r"\b(\S*?)(.)\2{2,}\b", r"")

    # text = re_sub(r"([^a-z0-9()<>'`\-]){2,}", allcaps)
    text = re_sub(r"([A-Z]){2,}", "")
    #eliminate punctuation
    text = re.compile('[%s]' % re.escape(string.punctuation)).sub('', text)
    
    return text.lower().strip()

class PreProcess():

    def _init_(self):
        return

    def fit( self, X, y = None ):
        return self

    def clean (self, x):
        cleaned_text = tokenize(x)
        return cleaned_text

    def transform(self, X, y = None):
        return X.apply(self.clean)