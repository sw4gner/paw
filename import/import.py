import sys
sys.path.append("..")

import tele_util

def importfile (filename, typ3):
    print('import %s\t%s' % (typ3, filename))
    errors = []
    with open(filename) as f:
        s = f.read()
    s = escape(s)
    i=0
    for l in s.split('\n'):
        sql = "INSERT INTO tod (type, text)value (%s,%s);"
        try:
            tele_util.executeSQL(sql, data=(typ3, l.encode('utf-8')))
            i+=1
        except:
            errors.append(l)
    print('finish import '+str(i))
    print(errors)
    return len(errors) == 0



def escape(s):
    s=s.replace('ü','ue')
    s=s.replace('ö','oe')
    s=s.replace('ä','ae')
    s=s.replace('Ü','Ue')
    s=s.replace('Ö','Oe')
    s=s.replace('Ä','Ae')
    return s



[importfile(*e) for e in [  ('would-you-rather.txt','r'),   # (508) lustig, pervers & extrem.
                            ('truth.txt','t'),              # (177) mischung aus allen kategorien
                            ('never-ever.txt','n'),         # (791) peinlich, schmutzig & ab 18
                            ('most-likely-to.txt','m'),     # (681) lustig, schmutzig, peinlich
                            ('dirty-truth.txt','i'),        # (52)  ...
                            ('dare.txt','d'),]]             # (123) mischung aus allen kategorien



