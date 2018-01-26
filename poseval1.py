#!/usr/bin/python

# =============================================================================
#  Version: 0.4 (Apr 2, 2009)
#  Authors: Antonio Fuschetto (fuschett@di.unipi.it), University of Pisa
#           Giuseppe Attardi (attardi@di.unipi.it), University of Pisa
# =============================================================================

# =============================================================================
#  This file is part of Tanl.
#
#  Tanl is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License, version 3,
#  as published by the Free Software Foundation.
#
#  Tanl is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================

"""\
Usage:
  poseval.py [options] gold-standard system-output

Options:
  -t ..., --train-file=...  : calculate accuracy on unknown words only (use
                              train file as known word dictionary)
  -e, --errors              : show tagging errors
  --help                    : display this help and exit
  --usage                   : display script usage
"""

import sys
import getopt
import re
import os.path

### CORE ######################################################################

def processData(goldFile, systemFile, trainFile, showDiff):
    goldList = goldFile.readlines()
    systemList = systemFile.readlines()
    
    knownWordList = []
    if trainFile:
        for line in trainFile:
            if not line.strip():
                continue
            form = line.split()[0].lower()
            if not form in knownWordList:
                knownWordList.append(form)
    
    if len(goldList) != len(systemList):
        print sys.stderr, 'Error: files have different lenght!'
        sys.exit(6)
    
    if showDiff:
        print '%5s  %-22s%-6s     %-9s' % ('#', 'FORM', 'GOLD', 'PREDICT')
        print '-' * (5 + 1 + 22 + 6 + 5 + 9)
    
    totalNo = 0
    correctNo = 0
    errorList = []
    
    for i in range(len(goldList)):
        if not goldList[i].strip():
            continue
        
        gold = goldList[i].split()
        system = systemList[i].split()
        
        if gold[0] != system[0]:
            print sys.stderr, 'Error: alignment error at line %d!' % (i + 1)
            sys.exit(7)
        
        if gold[0].lower() in knownWordList:
            continue
        
        totalNo += 1
        
        if gold[1] == system[1]:
            correctNo += 1
        else:
            if gold[1].startswith('SW'):
                errorList.append('SW')
            else:
                errorList.append(gold[1][0])
            
            if showDiff:
                print '%5d: %-22s%-6s --> %s' % (i + 1, gold[0], gold[1], \
                    system[1])
    
    if showDiff:
        print '-' * (5 + 1 + 22 + 6 + 5 + 9)
        print
    
    print 'Total:     %d' % totalNo
    print 'Corrects:  %d' % correctNo
    print 'Accuracy:  %.2f%%' % (correctNo * 100.0 / totalNo)
    
    totalErrNo        = len(errorList)
    adjectiveErrNo    = errorList.count('A')
    adverbErrNo       = errorList.count('B')
    conjunctionErrNo  = errorList.count('C')
    determinerErrNo   = errorList.count('D')
    prepositionErrNo  = errorList.count('E')
    punctuationErrNo  = errorList.count('F')
    interjectionErrNo = errorList.count('I')
    numeralErrNo      = errorList.count('N')
    pronounErrNo      = errorList.count('P')
    articleErrNo      = errorList.count('R')
    nounErrNo         = errorList.count('S')
    foreignnounErrNo  = errorList.count('SW')
    verbErrNo         = errorList.count('V')
    residualErrNo     = totalErrNo - (adjectiveErrNo + adverbErrNo + \
        conjunctionErrNo + determinerErrNo + prepositionErrNo + \
        punctuationErrNo + interjectionErrNo + numeralErrNo + pronounErrNo + \
        articleErrNo +  nounErrNo + foreignnounErrNo + verbErrNo)
    
    print '\n== Error statistics =='
    print '%-19s: %d' % ('adjectives (A)'    , adjectiveErrNo)
    print '%-19s: %d' % ('adverbs (B)'       , adverbErrNo)
    print '%-19s: %d' % ('conjunctions (C)'  , conjunctionErrNo)
    print '%-19s: %d' % ('determiners (D)'   , determinerErrNo)
    print '%-19s: %d' % ('prepositions (E)'  , prepositionErrNo)
    print '%-19s: %d' % ('punctuations (F)'  , punctuationErrNo)
    print '%-19s: %d' % ('interjections (I)' , interjectionErrNo)
    print '%-19s: %d' % ('numerals (N)'      , numeralErrNo)
    print '%-19s: %d' % ('pronouns (P)'      , pronounErrNo)
    print '%-19s: %d' % ('articles (A)'      , articleErrNo)
    print '%-19s: %d' % ('nouns (S)'         , nounErrNo)
    print '%-19s: %d' % ('foreign nouns (SW)', foreignnounErrNo)
    print '%-19s: %d' % ('verbs (V)'         , verbErrNo)
    print '%-19s: %d' % ('residuals'         , residualErrNo)

### USER INTERFACE ############################################################

def showHelp():
    print >> sys.stdout, __doc__,

def showUsage(outFile, scriptName):
    print >> outFile, 'Usage: %s [options] gold-standard system-output' % \
        scriptName

def showSuggestion(outFile, scriptName):
    print >> outFile, 'Try \'%s --help\' for more information.' % scriptName

def showFileError(scriptName, fileName):
    print >> sys.stderr, '%s: %s: No such file or directory' % (scriptName, \
        fileName)

def main():
    scriptName = os.path.basename(sys.argv[0])
    
    try:
        longOpts = ['help', 'usage', 'train-file', 'errors']
        opts, args = getopt.gnu_getopt(sys.argv[1:], 't:e', longOpts)
    except getopt.GetoptError:
        showUsage(sys.stderr, scriptName)
        showSuggestion(sys.stderr, scriptName)
        sys.exit(1)
    
    trainFile = None
    showDiff = False
    
    for opt, arg in opts:
        if opt == '--help':
            showHelp()
            sys.exit()
        elif opt == '--usage':
            showUsage(sys.stdout, scriptName)
            sys.exit()
        elif opt in ('-t', '--train-file'):
            try:
                trainFile = open(arg)
            except IOError:
                showFileError(scriptName, arg)
                sys.exit(2)
        elif opt in ('-e', '--errors'):
            showDiff = True
    
    if len(args) == 2:
        try:
            goldFile = open(args[0])
        except IOError:
            showFileError(scriptName, args[0])
            sys.exit(3)
        try:
            systemFile = open(args[1])
        except IOError:
            showFileError(scriptName, args[1])
            sys.exit(4)
    else:
        showUsage(sys.stderr, scriptName)
        showSuggestion(sys.stderr, scriptName)
        sys.exit(5)
    
    processData(goldFile, systemFile, trainFile, showDiff)
    
    goldFile.close()
    systemFile.close()

if __name__ == '__main__':
    main()
