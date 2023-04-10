import sys
import os
path = os.path.split(__file__)
newPath = path[0] + '/modules'
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.append(newPath)

from modules.verse_lexer import lexicon
