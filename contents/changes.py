#!usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import math
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

frame = []
#for line in open('unidia_top100nonunique.csv','rU'):
for line in open('unidia_full.csv','rU'):
  subframe = []
  for subline in line.split('\t'):
    subframe.append(subline.split())
  frame.append(subframe)

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

nuclei = ['a','aː','e','eː','i','iʔ','iː','o','oː','u','uʔ','uː''y','æ','ă','ĕ','ĩ','ŏ','ɐ','ɑ','ɑː','ɑ̆','ɒ','ə','əː','ə̆','ɛ','ɥ','ɨ','ɪ','ɪ̆','ʊ']

codas = ['b','bʰ','c','cʰ','d','dʰ','d̠͡ʒ','d̠͡ʒʰʲ','d͡z','f','fʰ','g','gʰ','gʲ','gʷ','gˀ','h','j','k','kʰ','kʷ','l','lʰ','m','mʰ','n','nʲ','p','pʰ','q','qˀ','r','s','t','tʰ','t̠͡ʃ','t̠͡ʃʰ','t̠͡ʃʰʲ','t̠͡ʃʲ','t͡s','t͡sʰ','v','w','x','xʰ','xʷ','z','ç','ŋ','ɓ','ɓˀ','ɓ̥ˀ','ɔ','ɕ','ɗ','ɗ̥ˀ','ɟ','ɠ̥ˀ','ɣ','ɣʰ','ɣʷ','ɱ','ɲ','ɾ','ʃ','ʄ','ʑ','ʒ','ʔ','ʔʲ','θ','ᶑ','ṕ','ṛ']

pairs = []

for i in range(0,len(nuclei)):
  for j in range(0,len(codas)):
    for k in range(0,len(nuclei)):
      pair = []
      base = ['#']
      deriv = ['#']
      base.append(nuclei[i])
      deriv.append(nuclei[i])
      base.append(codas[j])
      deriv.append('.')
      deriv.append(codas[j])
      base.append('#')
      deriv.append(nuclei[k])
      deriv.append('#')
      pair.append(' '.join(base))
      pair.append(' '.join(deriv))
      pairs.append(pair)

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

def pattern(pair): #NEEDS WORK
  syl = pair[1].split('.')[-1].split()[0]
  if syl in voi.keys() and pair[0].split()[-2] == voi[syl]:
    return 'voiced'
  if syl in devoi.keys() and pair[0].split()[-2] == devoi[syl]:
    return 'devoiced'
  if syl == pair[0].split()[-2] and syl in voi.keys() and pair[0].split()[-2] in voi.keys():
    return '-voi-voi'
  if syl == pair[0].split()[-2] and syl in devoi.keys() and pair[0].split()[-2] in devoi.keys():
    return '+voi+voi'
  else:
    return 'other'

def typer(tpl):
  k = defaultdict(int)
  for x in tpl:
    k[x]+=1
  if len(k.keys())==1:
    return 'yyy'
  elif len(k.keys()) < len(tpl):
    return 'xxy'
  elif len(k.keys()) == len(tpl):
    return 'xyz'

#def permy(array,k): #TO DO: fix this so that permutations can be generated and stored dynamically
#  final = defaultdict(int)
#  elm = defaultdict(int)
#  for x in array:
#    elm[x]+=1
#  working = ''
#  for x in sorted(elm.keys(),key=lambda(x):elm[x]):
#    if elm[x] > k:
#      working += x*k
#    else:
#      working += x*elm[x]
#  working = list(working)
#  for x in set(list(itertools.permutations(working,k))):
#    if typer(x) == 'xyz':
#      j = 1
#      for y in x:
#        j *= elm[y]
#      final[x] += j
#    elif typer(x) == 'xxy':
#      j = 1
#      for y in set(x):
#        for k in range(1, x.count(y)+1):
#          j *= elm[y] - k + 1
#      final[x] += j
#    elif typer(x) == 'yyy':
#      final[x] += math.factorial(elm[x[0]])/math.factorial(elm[x[0]]-k)
#  return final

def cool(k):
  weightdic = defaultdict(int)
  for x in list(itertools.permutations(weighted,k)):
    weightdic[x] += 1
  print 'weightdic generated'
  basedic = defaultdict(int)
  for x in list(itertools.permutations(baseline,k)):
    basedic[x] += 1
  print 'basedic generated'
  dicts = [weightdic,basedic]
  namelist = ['weightdic','basedic']
  f = open('results_'+str(k)+'.csv','w')
  for pair in pairs:
    for dic in dicts:
      for key in dic.keys():
#        print key
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
#        print changes
#        print pair
#        print '\t'.join(final)
        if pattern(final) != 'other':
          print >>f, str(namelist[dicts.index(dic)])+'\t'+str(dic.keys().index(key))+'\tpair '+str(pairs.index(pair))+'\t'+'|'.join(final)+'\t'+str(pattern(final))+'\t'+str(dic[key])
    print str(pairs.index(pair))+' done',

  f.close()

  print 'done with %i' % n

def main():
  if len(sys.argv) != 2:
    print 'usage: ./changes.py [permutation length]'
    sys.exit(1)
  else:
    k = int(sys.argv[1])
    cool(k)

if __name__ == "__main__":
  main()
