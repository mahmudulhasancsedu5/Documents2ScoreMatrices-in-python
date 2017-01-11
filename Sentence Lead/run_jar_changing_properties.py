
import subprocess

import os

from os import fsync
import re

import time

from pyjavaproperties import Properties





def runJar(path):
    subprocess.call(['java', '-jar', 'rouge2.0_0.2.jar'])

def getDirList(path):
    all_subDir= next(os.walk(path))[1]
    return all_subDir
    

def createResult(path):
    all_dir=getDirList(path)

    varss=['project.dir','outputFile']
    vars2=['outputFile','project.dir']
    for x in all_dir:
        print x
        p = Properties()
        p.load(open('rouge.properties'))

        for name, value in [('project.dir', x), ('outputFile', str(x+'_results.csv'))]:
            p[name] = value
            
        p.store(open('rouge.properties', 'w'))
        
        #time.sleep(30)
        runJar(path)
        



Dir="F:\\Education\\4_2\\Thsis\\python_sentence_vector_creation\\Sentence Lead\\"

createResult(Dir)

runJar(Dir)
