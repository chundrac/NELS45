#!usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import re
import itertools
import codecs
import random
from collections import defaultdict

#voi[-voi] = [+voi] : returns the voiced version of voiceless key
voi = {'\xc9\xb8': '\xce\xb2', 'c': '\xc9\x9f', 'f': 'v', 'k': 'g', '\xc9\x95': '\xca\x91', '\xce\xb8': '\xc3\xb0', 'p': 'b', '\xca\x88': '\xe1\xb6\x91', 't': 'd', 'x': '\xc9\xa3', '\xca\x82': '\xca\x90', '\xca\x83': '\xca\x92'}

#voi[+voi] = [-voi] : returns the voiceless version of voiced key
devoi = {'b': 'p', 'd': 't', 'g': 'k', '\xca\x90': '\xca\x82', '\xe1\xb6\x91': '\xca\x88', '\xca\x92': '\xca\x83', '\xca\x91': '\xc9\x95', 'v': 'f', '\xce\xb2': '\xc9\xb8', '\xc3\xb0': '\xce\xb8', '\xc9\xa3': 'x', '\xc9\x9f': 'c'}

#read unidia rows
#convert into strings

frame = [] #array: for a rule A > B / _C, each row contains A|B|C
for line in open('unidia_pilot_use.csv','rU'):
  subframe = []
  for subline in line.split('\t'):
    subframe.append(subline.split())
  frame.append(subframe)

for line in frame:             #converts null set symbol to empty item in list
  for subline in line:
    for string in subline:
#      if str == u'\u2205': '''UNICODE'''
      if string == '\xe2\x88\x85':
        k = subline.index(string)
        subline.pop(k)
        subline.insert(k,'')

weighted = []
for line in frame:
  row = []
  for subline in line:
    row.append(';'.join(subline))
  weighted.append('|'.join(row))

baseline = []
for line in weighted:
  if line not in baseline:
    baseline.append(line)
  else:     #probably
    continue#redundant

#vowels and consonants capable of instantiating final obstruent voicing/devoicing
#stuff = [['p', 'b', 'f', 'v', '\xc9\xb8', '\xce\xb2', 't', 'd', '\xce\xb8', '\xc3\xb0', 'k', 'g', 'x', '\xc9\xa3', '\xca\x88', '\xe1\xb6\x91', '\xca\x82', '\xca\x90', 'c', '\xc9\x9f', '\xca\x83', '\xca\x92', '\xc9\x95', '\xca\x91'], ['a', '\xc9\x9b', 'e', '\xc9\xaa', 'i', 'o', 'u', 'y', '\xc9\x99']]

stuff = [['t\xcd\xa1s', '\xc9\x93\xcc\xa5\xcb\x80', 's\xca\xb2', 's\xca\xb0', 'q\xcb\x80', 's\xca\xb7', 'k\xca\xb2', 'k\xca\xb0', 'm\xca\xb0', 'k\xca\xb7', 'k\xca\xbc', 'p\xca\xbc', 's\xca\xbc', 'c', '(x)', '(g)', 'n\xcc\xaa', '\xca\x94\xca\xb2', 'd\xcc\xa0\xcd\xa1\xca\x92\xca\xb0\xca\xb2', '\xce\xb8', '\xce\xb2', 'd', '(\xc9\xbd)', 'r\xcc\xa5', 'h', 'l', 'p', '\xc9\x93\xcb\x80', 't', 'x', 'k\xcd\xa1p', 'd\xca\xb2', '\xc9\x9f', '\xc9\x93', '\xc9\x95', '\xca\x88\xcd\xa1\xca\x82\xca\xb0', '\xc9\x9f\xcd\xa1\xca\x91', '(j)', '\xc9\xb9', '\xc9\xb8', '\xca\x83\xca\xb0', '\xc9\xbe', '\xc9\xb1', '\xc9\xb2', '\xc9\xb4', '(r)', '\xc9\xac', '\xc9\xae', '\xc9\xa3', '\xc9\xa5', 't\xcc\xa0\xca\xb0\xca\xb2', '\xca\x88\xcd\xa1\xca\x82', '(k)', 't\xcc\xa0\xca\xb2', 'f\xca\xb0', 'k\xca\xb0\xca\xb2', 'k\xcb\x80', 'h\xca\xb7', 't\xcd\xa1s\xca\xb2', '(b)', 'h\xca\xb0', 'g', 'm\xcb\x80', 'k', 's', 'b\xca\xb2', 't\xcd\xa1r', 'l\xcc\xa0', '(\xc9\xa3)', 't\xcc\xa0\xcd\xa1\xca\x83\xca\xb0\xca\xb2', '(t)', '\xc9\x97\xcc\xa5\xcb\x80', '(l)', 't\xcc\xaa', 'c\xca\xb0', 'k\xca\xbc\xca\xb7', 't\xcc\xa0\xcd\xa1\xca\x83', 'c\xca\xb7', 'f\xca\xb7', '\xc3\xa7', '\xe1\xb6\x91', 'd\xcd\xa1r', 't\xcc\x81', 'd\xcd\xa1z', 'g\xcb\x80', '\xc3\xb1', '\xc3\xb0', '\xca\x94', 'g\xca\xb7', '(\xe1\xb9\x9b)', 'g\xca\xb2', '\xca\x91', 'g\xca\xb0', 'N', '\xc9\x97', '\xca\x84', '\xc5\x8b\xca\xb2', '\xca\x82', '\xca\x83', 'b', 'f', 't\xcd\xa1s\xe2\x81\xbf', 'j', 'n', 'r', 'v', 't\xcd\xa1s\xca\xb0', 'z', '\xc8\xb8\xcd\xa1v', '\xc5\x8b', '(m)b', '\xc9\xa3\xca\xb2', '\xe1\xb9\x95', '\xc9\xa3\xca\xb0', '\xc9\xa3\xca\xb7', '\xe1\xb9\x9b', 'l\xca\xb2', '\xc9\xa1\xcd\xa1b\xca\xb7', 'd\xcc\xa0\xcd\xa1\xca\x92', 'd\xcd\xa1z\xcb\x9e', 'p\xca\xb0\xca\xb2', 'k\xca\xb7\xca\xb0', 'k\xca\xb7\xca\xb2', 'n\xca\xb2', 'k\xcc\x9a', '\xc9\xa1\xcd\xa1b', 'n\xcb\x80', 'w', 'w\xcc\xb0', '\xca\x90', '\xc8\xb9\xcd\xa1f', 'x\xca\xb7', '\xca\x92', 'x\xca\xb0', 'c\xcd\xa1\xc9\x95', 'c\xcb\x80', 't\xcc\xa0\xcd\xa1\xca\x83\xca\xb0', 't\xcc\xa0\xcd\xa1\xca\x83\xca\xb2', 'm', '\xe1\xb8\xbf', 't\xca\xbc', 'q', 't\xca\xb0', '\xc9\xa0\xcc\xa5\xcb\x80', 'p\xca\xb0', 'p\xca\xb2'], ['\xe1\xb9\xbc', '\xe1\xbb\xb9', '\xc9\x9b\xcb\x90', 'u(\xcb\x90)', '\xc9\x99\xcc\x86', '\xc9\x91\xcc\x86', '\xc9\x99', '\xc9\x9b', '\xc9\x91', '\xc9\x90', '\xc9\x94', '\xc9\xa8', '\xc9\xaa', 'o\xcb\x90', 'o', 'u\xcb\x90', '\xca\x8a\xcb\x90', 'i(\xcb\x90)', 'i\xcb\x90', '\xc9\xaa\xcc\x86', '\xc3\xa9', '\xc3\xad', '\xc3\xa1', '\xc9\x99\xcb\x90', '\xc3\xb3', '\xca\x8a', '\xc9\x94\xcb\x90', 'i', '\xc5\x8f', 'u\xcc\x9d', '\xc5\x93', '\xc5\xa9', '\xc5\xb7', 'a', 'i\xcc\x9d', 'e', '\xc4\xa9', 'a\xcb\x90', 'u', 'y', 'e\xcb\x90']]

#vowels and consonants to be randomly chosen
segs = {'C': ['\xca\x83', '\xcc\x86', '\xe1\xb6\x91', '\xcc\x9a', '(', '\xcc\xaa', ',', '\xca\xb7', '\xc8\xb8', '\xc9\xa0', 'd', '\xc3\xa7', 'h', '\xc9\xac', 'p', 't', '\xc9\xb8', '\xe1\xb9\xbc', '\xcc\x81', 'j', '\xca\x84', '\xca\x88', 'l', '\xca\x90', '\xca\x94', '\xc9\xae', '\xcc\x9d', '\xca\xb0', '\xce\xb2', '\xca\xbc', '\xe1\xb8\xbf', '\xc9\xb4', '\xcb\x80', '\xc9\x93', '\xc9\x97', 'x', '\xe1\xb9\x9b', 'r', '\xc9\x9f', '\xcd\xa1', '\xc9\xa3', 'g', 'k', '\xc3\xb0', 's', 'w', '\xe1\xb9\x95', '\xc9\xbe', '\xe2\x81\xbf', '\xca\x91', '\xc9\xa1', 'c', 'N', 'b', 'f', 'n', '\xc3\xb1', '\xc9\xb2', 'v', 'z', '~', '\xca\x82', '\xca\x92', '\xc9\xb1', ')', '\xca\xb2', '\xc8\xb9', '\xce\xb8', '\xc5\x8b', '\xc9\x95', '\xcb\x9e', 'm', 'q', '\xcc\xa9', '\xc9\xb9', '\xc9\xbd'], 'V': ['\xc9\x90', '\xc9\x94', '\xc3\xb3', '\xc9\xa8', '\xe1\xb9\xbc', '\xc4\xa9', '\xcb\x90', '\xc5\xa9', 'o', '\xc9\x9b', '\xcc\xa0e', '\xc3\xa1', '\xc3\xa9', '\xc9\xaa', '\xc3\xad', '\xe1\xbb\xb9', '\xca\x8a', '\xc5\x8f', '\xc9\x91', 'y', '\xc5\x93', '\xc9\x99', '\xcb\x9e', 'a', '\xc9\xa5', 'i', 'u', '\xc5\xb7']}

pairs = []          #Generate CVCVC ~ CVCVCV pairs, where final VC(V) include all logically possible sequences of the segments in list 'stuff'

for i in range(0,len(stuff[1])):
  for j in range(0,len(stuff[0])):
    for k in range(0,len(stuff[1])):
      pair = []
      base = ['#']
      deriv = ['#']
      a = random.sample(xrange(len(stuff[0])),1)[0]
      b = random.sample(xrange(len(stuff[1])),1)[0]
      c = random.sample(xrange(len(stuff[0])),1)[0]
      d = random.sample(xrange(len(stuff[0])),1)[0]
      base.append(stuff[0][a])
      deriv.append(stuff[0][a])
      base.append(stuff[1][b])
      deriv.append(stuff[1][b])
      if random.sample(xrange(2),1)[0] == 1:
        base.append(stuff[0][c])
        deriv.append(stuff[0][c])
      base.append('.')
      deriv.append('.')
      base.append(stuff[0][d])
      deriv.append(stuff[0][d])
      base.append(stuff[1][i])
      deriv.append(stuff[1][i])
      base.append(stuff[0][j])
      deriv.append('.')
      deriv.append(stuff[0][j])
      base.append('#')
      deriv.append(stuff[1][k])
      deriv.append('#')
      pair.append(' '.join(base))
      pair.append(' '.join(deriv))
      pairs.append(pair)

print 'pairs done; initializing'

def trans(str,inlist,outlist,envir):
  initial = str.split()      #converts whitespace-delimited input string into list
  final = []                 #puts output list here
  k = len(inlist)
  if inlist == 2*['']:       #normalizes blank inputs
    inlist.pop(-1)
  if envir == ['']:
    envir = []
  if len(envir) == 0:
    envir = ['_']
  envir = [envir[:envir.index('_')],envir[envir.index('_')+1:]]                   #splits envir into 2 lists containing elements on each side of '_'
  l = len(envir[0])
  m = len(envir[1])
  if len(envir[0]) > 0:
    if envir[0][0] == '.':      #converts str's initial '#' to initial '.' if conditioning environment contains initial syllable rather than word boundary
      initial.pop(0)
      initial.insert(0, '.')
  if len(envir[-1]) > 0:
    if envir[-1][-1] == '.':    #converts str's initial '#' to initial '.' if conditioning environment contains initial syllable rather than word boundary
      initial.pop(-1)
      initial.append('.')
  sylcounter = 0
  for line in envir:
    for word in line:
      if '.' in word:
        sylcounter += 1
  if sylcounter == 0:           #if there are no prosodically conditioned rules, temporarily get rid of syllable boundaries
    sylbounds = []
    for i,word in enumerate(initial):
      if initial[i] == '.':
        sylbounds.append(i) #get their indices, so they can be re-inserted later
    for word in initial:
      if word == '.':
        initial.pop(initial.index(word))
  for word in inlist:
    if len(word) == 0:          #if there is a blank entry in A (usually in prothetic/epenthetic/paragogic rules), e.g., ['','j'] > ['g','j']
      tempin = []
      for word in inlist:
        if len(word) > 0:
          tempin.append(word)
      ins = []
      for i,string in enumerate(initial):
        for j in range(0, len(tempin)):
          if initial[i-j:i+len(tempin)-j] == tempin:
    	    ins.append(i-j+inlist.index(''))
      for i in reversed(ins):
        initial.insert(i,'')     #puts relevant blank entry in the input string
  for i,string in enumerate(initial):                     #looks for environment
    counter = 0
    for j in range(0,len(inlist)):
      if initial[i-j-l:i-j] == envir[0][0:l] and initial[i-j+k:i-j+k+m] == envir[1][0:m]:
        if initial[i-j:i+len(inlist)-j] == inlist:
          counter += 1
          final.append(outlist[j])
#        if inlist == ['']:
#          counter += 1
#          if len(envir[0]) > len(envir[1]):
#            for word in outlist:
#              final.append(word)
#            final.append(initial[i])
#          if len(envir[0]) < len(envir[1]):
#            final.append(initial[i])
#            for word in outlist:
#              final.append(word)
 #         if len(envir[0]) == len(envir[1]):
 #           if initial[i-1:i] == envir[0][0] and initial[i:i+1] == envir[1][0]:
 #             initial.insert(i,'')
 #           final.append(initial[i])
 #           for word in outlist:
 #             final.append(word)
      if i > 0:
        if inlist == [''] and initial[i-j-l:i-j] == envir[0][0:l] and initial[i-j:i-j+m] == envir[1][0:m]: #for rules like [''] > ['l'] / ['a','_','a'], if they exist
          counter += 1
          for word in outlist:
            final.append(word)
          final.append(initial[i])
    if counter != 1:
      final.append(initial[i])
  if final[0] == '.':               #Changes if syllable boundary back to word boundary, if relevant
    final.pop(0)
    final.insert(0,'#')
  if final[-1] == '.':              #Changes if syllable boundary back to word boundary, if relevant
    final.pop(-1)
    final.append('#')
  if sylcounter == 0:
#    for i in reversed(sylbounds):
    for i in sylbounds:
      final.insert(i,'.')
  for word in final:
    if word == '':                  #gets rid of blank entries
      final.pop(final.index(word))  #
  return ' '.join(final)

#trans('# a p a #',['a'],['i'],[''])

def pattern(pair): #NEEDS WORK
  syl = pair[1].split('.')[-1].split()[0]
  if syl in voi.keys() and pair[0].split()[-2] == voi[syl]:
    return 'voiced'
  if syl in devoi.keys() and pair[0].split()[-2] == devoi[syl]:
    return 'devoiced'
  if syl == pair[0].split()[-2]:
    return 'same'
  else:
    return 'other'

def cool(numb):

  weightdic = defaultdict(int)

  for x in list(itertools.permutations(weighted,numb)):
    weightdic[x] += 1

  print 'weightdic generated'

  basedic = defaultdict(int)

  for x in list(itertools.permutations(baseline,numb)):
    basedic[x] += 1

  print 'basedic generated'

  dicts = [weightdic,basedic]

  namelist = ['weightdic','basedic']

  f = open('tester_'+str(numb)+'.csv','w')
  for pair in pairs:
    for dic in dicts:
      for key in dic.keys():
        changes = []
        for string in key:
          change = []
          for substring in string.split('|'):
            change.append(substring.split(';'))
          changes.append(change)
        final = []
        for word in pair:
          tweaked = ''
          tweaked += word
          for line in changes:
            tweaked = trans(tweaked,line[0],line[1],line[2])
          final.append(tweaked)
        if pattern(final) == 'voiced' or pattern(final) == 'devoiced':
          for i in range(0,dic[key]):
            print >> f, str(pairs.index(pair))+'\t'+str(pattern(final))+'\t'+str(namelist[dicts.index(dic)])

  f.close()

  print 'we done with %i, homie' % numb

def main():
  if len(sys.argv) != 2:
    print 'usage: ./simchange.py \'list of input words (in quotes, delimited by space), e.g., rat raden tak tage\''
    sys.exit(1)
  else:
    numb = int(sys.argv[1])
    cool(numb)

if __name__ == "__main__":
  main()
