from functools import *

syntax = [
    ['AC = MQ', '0A %x'],
    ['AC = -(Mem[%s])', '02 %x'],
    ['AC =  Mem[%s]', '01 %x'],
    ['AC =  abs(Mem[%s])', '03 %x'],
    ['AC += Mem[%s]', '05 %x'],
    ['AC += abs(Mem[%s])', '07 %x'],
    ['AC -= Mem[%s]', '06 %x'],
    ['AC -= abs(Mem[%s])', '08 %x'],
    ['AC *= 2', '14 %x'],
    ['AC /= 2', '15 %x'],
    ['MQ =  Mem[%s]', '09 %x'],
    ['MQ =  AC / Mem[%s]; AC %= Mem[%s]', '0C %x'],
    ['MQ *= Mem[%s]', '0B %x'],
    ['goto(%s[0])', '0D %x'],
    ['goto(%s[1])', '0E %x'],
    ['goto(%s[0]) if AC >= 0', '0F %x'],
    ['goto(%s[1]) if AC >= 0', '10 %x'],
    ['Mem[%s][0] = AC[1]', '12 %x'],
    ['Mem[%s][1] = AC[1]', '13 %x'],
    ['Mem[%s] = AC', '21 %x']
]
nnssyntax = [
    ['AC=MQ', '0A %x'],
    ['AC=-(Mem[%s])', '02 %x'],
    ['AC=Mem[%s]', '01 %x'],
    ['AC=abs(Mem[%s])', '03 %x'],
    ['AC+=Mem[%s]', '05 %x'],
    ['AC+=abs(Mem[%s])', '07 %x'],
    ['AC-=Mem[%s]', '06 %x'],
    ['AC-=abs(Mem[%s])', '08 %x'],
    ['AC*=2', '14 %x'],
    ['AC/=2', '15 %x'],
    ['MQ=Mem[%s]', '09 %x'],
    ['MQ=AC/Mem[%s];AC%=Mem[%s]', '0C %x'],
    ['MQ*=Mem[%s]', '0B %x'],
    ['goto(%s[0])', '0D %x'],
    ['goto(%s[1])', '0E %x'],
    ['goto(%s[0])ifAC>=0', '0F %x'],
    ['goto(%s[1])ifAC>=0', '10 %x'],
    ['Mem[%s][0]=AC[1]', '12 %x'],
    ['Mem[%s][1]=AC[1]', '13 %x'],
    ['Mem[%s]=AC', '21 %x']
]


def extract(a, src, b):
    if a in src:
        src = src[src.find(a) + len(a):]
    if b in src:
        src = src[:src.find(b)]
    return src


def pattern_extract(src, model, pattern):
    tk = model.split(pattern)
    resp = []
    for i in range(1, len(tk)):
        resp.append(extract(tk[i - 1], src, tk[i]))
    return resp


def translate(instr):
    for nns in nnssyntax:
        nnssplit = nns[0].split('%s')

        if reduce(lambda x, y: x and y, [s in instr for s in nnssplit]):
            x = pattern_extract(instr, nns[0], '%s')[0]
            return nns[1].replace('%x', x)


def file_manager(src_file_name, out_file_name):
    max = 1023
    i, j = 0, 0
    with open(out_file_name, 'w') as out, open(src_file_name, 'r', encoding='utf-8') as src:
        out_line = ''
        map = []
        for line in src:
            line = ''.join(line.split(' '))
            if line.startswith('data'):
                line = line[4:]
                map.append(line.split('='))
            else:
                for m in range(len(map)):
                    line = line.replace(map[m][0], 'Mem[{0}]'.format(format(max - m, '03x').upper()))
                i += 1
                for instr in line.split(';'):
                    if out_line == '':
                        out_line = format(j, '03x').upper() + ' '
                    elif len(out_line) <= len('008 01 3FC 0E 400'):
                        out_line += ' ' + translate(instr)
                        j += 1
                    else:
                        out.write(out_line)
                        out_line = ''
        for k in range(len(map)):
            out.write(format(max - m, '03x').upper() + ' ' + format(map[m][1], '10x').upper())


src_file_name = input('Type the src file name: ')
out_file_name = input('Type the out file name: ')
file_manager(src_file_name, out_file_name)