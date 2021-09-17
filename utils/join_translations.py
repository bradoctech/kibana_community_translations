#!/usr/bin/python

import collections
import glob
import json
import os


def join_translation(iso_code, output_filename):
    files = glob.glob('plugins/*/%s.json' % (iso_code))
    files = files + glob.glob('plugins/xpack/*/%s.json' % (iso_code))

    messages = dict()
    
    for filename in files:
        content = json.load(open(filename, encoding='utf-8'))
        messages.update(content)
        
        
    formats = []
    
    format_filename = os.path.join('plugins', iso_code + '_formats.json')
    if os.path.isfile(format_filename):
        formats = json.load(open(format_filename, encoding='utf-8'))

    messages = collections.OrderedDict(
        sorted(messages.items(), key=lambda x:x[0].lower())
    )

    data = {
        'formats': formats,
        'messages': messages
    }
            
    with open(output_filename, 'w', encoding='utf-8') as handler:
        json.dump(data, handler, indent=2)


if __name__ == '__main__':
    translations = json.load(open('.i18nrc.json'))
    files = translations['translations']

    for file in files:
        print ('Generating', file, '...')

        filename = os.path.basename(file)
        iso_code = filename.replace('.json', '')

        join_translation(iso_code, file)
