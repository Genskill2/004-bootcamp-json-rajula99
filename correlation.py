# Add the functions in this file
import json
import math

def load_journal(fname):
    f = open(fname,)
    data = json.load(f)
    #l = list(data)
    f.close()
    return data

def compute_phi(fname, event):
    journal_list = load_journal(fname)
    n11, n00, n10, n01 = 0, 0, 0, 0
    for d in journal_list:
        if event in d['events']:
            if d['squirrel'] == True:
                n11 += 1 
            else:
                n10 += 1
        elif d['squirrel'] == True:
            n01 += 1
        else:
            n00 += 1
    n1p = n11 + n10
    n0p = n01 + n00
    np0 = n00 + n10
    np1 = n11 + n01
    corr = (n11 * n00 - n10 * n01) / math.sqrt(n1p * n0p * np1 * np0)
    return corr


def compute_correlations(fname):
    journal_list = load_journal(fname)
    event_d = dict()
    for d in journal_list:
        for event in d['events']:
            if event not in event_d.keys():
                e_corr = compute_phi(fname, event)
                event_d[event] = e_corr
    return event_d


def diagnose(fname):
    d = compute_correlations(fname)
    key_list = list(d.keys())
    val_list = list(d.values())
    hp = val_list.index(max(val_list))
    hp_event = key_list[hp]
    hn = val_list.index(min(val_list))
    hn_event = key_list[hn]
    return hp_event, hn_event