#!/usr/bin/python

import collections
import glob
import json
import os


def break_translation(iso_code):
    src = os.path.join('translations', iso_code + '.json')
    
    try:
        translated = json.load(open(src, encoding='utf-8'))
    except:
        return;
    
    groups = collections.defaultdict(dict)

    
    for key in translated['messages'].keys():
        subkeys = key.split('.')
        prefix = subkeys[0]
        
        if prefix == 'xpack':
            prefix = prefix + '.' + subkeys[1]

        groups[prefix][key] = translated['messages'][key]
        
    
    for key in groups.keys():
        messages = groups[key]
        
        if '.' in key:
            key = key.split('.')
            dirname = os.path.join('plugins', key[0], key[1])
        else:
            dirname = os.path.join('plugins', key)

        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        filename = os.path.join(dirname, iso_code + '.json')
        with open(filename, 'w') as handler:
            json.dump(messages, handler, indent=2, sort_keys=True)

    filename = os.path.join('plugins', iso_code + '_formats.json')
    with open(filename, 'w') as handler:
        json.dump(translated['formats'], handler, indent=2, sort_keys=True)



if __name__ == '__main__':
    translations = json.load(open('.i18nrc.json'))
    files = translations['translations']

    for file in files:
        print ('Breaking', file, '...')

        file = os.path.basename(file)
        iso_code = file.replace('.json', '')

        break_translation(iso_code)
