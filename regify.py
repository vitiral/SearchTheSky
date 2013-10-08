# -*- coding: utf-8 -*-
"""
This code is made to mimick Kiki but with additional features. This is a similar
method of text handling that I used with wordTeX -- and I think it is my favorite.
Turn everything into the text into objects -- it only works if everything is 
mututally exclusive, which fortunately it is with Regexp. (all groups contain
more groups -- but a found group is never part of another group). 

If this were not true, then doing substitutions on regular expressions would be
impossible (how would you substitute two over-lapping expressions?)


"""
import pdb
import sys
sys.path.insert(1, '..')
from cloudtb import dbe

import re


def objectify(text, regexp):
    stop = 0
    if type(regexp) == str:    
        regexp = re.compile(regexp)
    data_list = []
    match = 0
    while True:
        searched = regexp.search(text, stop + 1)
        if searched == None:
            data_list.append(text[stop:])
            return data_list
        groups = searched.groups()
        start, stop = searched.span()
        new_reobj = reobj(groups, 0, match = match, regcmp = regexp)
        upd_val, null = new_reobj.update()
        assert(upd_val == len(groups))
        data_list.append(new_reobj)
        match += 1

class reobj(object):
    def __init__(self, groups, index, match = None, regcmp = None):
        self.groups = groups
        self.index = index
        self.text = groups[index]
        self.data_list = None
        self.match = match
        self.regcmp = regcmp
        self.is_updated = False
        assert(self.text == groups[self.index])
    
    def update(self):
        '''Goes through it's own text and figures out if there
        are any groups inside of itself. Returns the index + 1 of the
        last group it finds'''
        assert(not self.is_updated)
        text, groups = self.text, self.groups
        data_list = []
        end_i = 0
        # recursive function. The index increments on each call to itself
        index = self.index + 1
        while index < len(groups):
            gtxt = groups[index]
            if gtxt == None:
                index += 1
                continue
            begin_i = text.find(gtxt, end_i)#+1 if end_i != 0 else 0)
            if begin_i == -1:
                assert(end_i == 0)
                assert(len(data_list) == 0)
                if text == '.':
                    pdb.set_trace()
                data_list = [text]
                end_i = len(text)
                break
            data_list.append(text[end_i:begin_i]) # append raw text in between
            end_i = begin_i
            new_reobj = reobj(groups, index)
            index, end_i_obj = new_reobj.update()
            end_i += end_i_obj
            data_list.append(new_reobj)
        else:
            # index went above bounds.
            if not data_list:   # you never even entered the loop
                data_list = [text]
                end_i = len(text)
            else:
                # need to add final bits of text.
                data_list.append(text[end_i:])
            
        self.is_updated = True
        self.data_list = [n for n in data_list if n != '']
        return index, end_i
    
    def __repr__(self):
        start = ''
        if self.match != None:
            start = '{{{0}}}'.format(self.match)
        str_data = ''.join([str(n) for n in self.data_list])
        return start + '({0})<P{1}>'.format(str_data, self.index)

if __name__ == '__main__':
    text = '''
    Chapman: I didn't expect a kind of Spanish Inquisition. 
    (JARRING CHORD - the cardinals burst in) 
    Ximinez: NOBODY expects the Spanish Inquisition! Our chief weapon is surprise...surprise and fear...fear and surprise.... Our two weapons are fear and surprise...and ruthless efficiency.... Our *three* weapons are fear, surprise, and ruthless efficiency...and an almost fanatical devotion to the Pope.... Our *four*...no... *Amongst* our weapons.... Amongst our weaponry...are such elements as fear, surprise.... I'll come in again. (Exit and exeunt)
    '''
    regexp = r'''(([a-zA-Z']+\s)+?expect(.*?)(the )*Spanish Inquisition(!|.))'''
    
    rcmp = re.compile(regexp)
    se = rcmp.search(text)
    dl = objectify(text, rcmp)
    
    print ''.join([str(n) for n in dl])

        
        