import re
from random import randint

p_dice = re.compile('([+-]{0,1})(\d*)d(\d+)(\*?\~?)')
p_mod = re.compile('(?<!d)([+-])(\d+)(?!d)')

def getrol (adv=None, prn=True):
    def retfun(dice):
        roll1 = randint(1,dice)
        roll2 = randint(1,dice)
        if adv == None:
            rs = roll1
            out = 'd%i -> %i' % (dice, roll1)
        if adv == True:
            rs = max(roll1, roll2)
            out = 'd%i adv. (%i, %i) -> %i' % (dice, roll1, roll2, rs)
        if adv == False:
            rs = min(roll1, roll2)
            out = 'd%i dis. (%i, %i) -> %i' % (dice, roll1, roll2, rs)
        return (rs, out)
    return retfun	

def roll(term, out=[], adv=False):
    sum = 0
    itr = p_dice.finditer(term)
    for m in itr:
        rol_adv = (True if adv or '*' == m.group(4) else False if '~' == m.group(4) else None)
        f = getrol(rol_adv)
        val, txt = rslvroll(f, m.group(1), m.group(2), m.group(3))
        out += txt 
        sum += val
    itr = p_mod.finditer(term)
    mod=0
    for m in itr:
        sign = -1 if '-' == m.group(1) else 1
        mod += (sign*int(m.group(2)))
    if mod > 0:
        out += ('mod -> %i\n' % mod)
    sum += mod
    out = list('*%s = %i*\n\n' % (term, sum)) + out
    return sum, out

def rslvroll(f_roll, sign, qnt, dice):
    sign = -1 if sign=='-' else 1
    try:
        qnt = int(qnt)
    except ValueError:
        qnt = 1
    try:
        dice = int(dice)
    except ValueError:
        return 0 , ['%s ist kein gültiger Wurf' % dice]
    sum = 0
    sums =[]
    txt =[]
    for i in range(qnt):
        val, txt_rol = f_roll(dice)
        sum+=val
        sums.append(val)
        txt+=txt_rol
    return sign * sum, '%sd%s -> %s => %s\n' % (qnt, dice, sums, sum)