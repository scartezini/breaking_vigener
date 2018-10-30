#!/usr/bin/python
import sys
import numpy as np
import itertools
import operator


def decrypt(msg, key):
    res = []
    i = 0
    for m in msg:
        res.append( chr(m ^ ord(key[i])))
        i = (i + 1) % len(key)

    return res



def most_common(L):
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(L))
  # print 'SL:', SL
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
     #print ('item %r, count %r, minind %r' % (item, count, min_index))
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]


def discovery_key(freq, guess):
    k = []
    for i in range(0, len(freq)):
        k.append(chr(int(freq[i]) ^ ord(guess[i]) ))

    return k

if __name__ == '__main__':
    try:
        file = open(sys.argv[1], "r")
    except:
        sys.exit("Passar arquivo com a cifra como argumento")

    print (file.readline())
    print (file.readline())

    crypto = []
    line = file.readline()
    while line != '\n':
        crypto.append(int(line))
        line = file.readline()

    distance = []
    for i in range(0, len(crypto)):
        for j in range(i+1, len(crypto) - 1):
            if crypto[i] == crypto[j] and crypto[i+1] == crypto[j+1]:
                distance.append((j-i))

    print(distance)

    #calcular mdc entre todos os valores de distance

    mdc = 7 #caso da cifra
    parts = np.zeros( (mdc, int(len(crypto)/mdc)+1 ) )
    for i in range(0, len(crypto)):
        parts[i%mdc][int(i/mdc)] = crypto[i]

    print(parts)
    freq = []
    for i in range(0, mdc):
        freq.append(most_common(parts[i]))

    print(freq)

    guess = ['e',' ','e',' ',' ',' ',' ']
    key = discovery_key(freq, guess)
    print(key)


    f = open('msg.txt','w')
    msg = decrypt(crypto, key)
    i = 0
    print(msg)
    for m in msg:
        f.write("%c - %d\n" % (m, i))
        i = (i + 1) % mdc

    for m in msg:
        sys.stdout.write(m)
