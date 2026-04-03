import csv
from datetime import datetime
from collections import OrderedDict, Counter
import json
import sys
import operator
import re

# TODO:
# - how many cannot play sound?
# - how much right/wrong per field


field_ids_to_titles = {
    17: 'Wahrnehmung oder nicht?',
    16: 'Welche Bewertung passt dazu?',
    15: 'Was zeigt das Foto?',
    14: 'Welche Wahrnehmung passt dazu?',
    12: 'Gefühl oder nicht?',
    20: 'Welche sind Gefühle?',
    19: 'Gefühle darstellen',
    11: 'Welches Gefühl ist das?',
    9:  'Bedürfnis oder nicht?',
    8:  'Welche Strategie passt hier?',
    7:  'Um welches Bedürfnis geht es?',
    6:  'Welches Bedürfnis passt hier?',
    4:  'Ist das eine sinnvolle Bitte?',
    3:  'Gibt es hier riskante Wörter?',
    2:  'Tangram',
    1:  'Warum ist die Bitte nicht sinnvoll?',
    18: 'Was passt hier nicht?',
    13: 'Wie wurde das gehört?',
    10: 'Im Wolfscafé',
    5:  'Ist das eine empathische Vermutung?'
}

def read_logfile(filename):
    return [json.loads(line) for line in open(filename)]

def parsets(d):
    return datetime.strptime(d['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')

def delta_to_seconds(first, last):
    d = last - first
    return d.days * 24 * 60 * 60  + d.seconds


def format_field_dict(d):
    d = d.copy()
    none_count = d.pop(None)
    for k, v in reversed(sorted(d.items(), key=operator.itemgetter(1))):
        print('  ', field_ids_to_titles[k]+ ':', v)
    print('  None:', none_count)


def write_field_dict_to_csv(title, d, csv_file):
    d = d.copy()
    none_count = d.pop(None)
    for k, v in reversed(sorted(d.items(), key=operator.itemgetter(1))):
        csv_file.writerow([title, field_ids_to_titles[k], v])
        title = ''


def get_method_count(log_lines, stats_csv):
    total = 0
    method_count = {}

    for line in log_lines:
        if 'method' in line:
            method_count.setdefault(line['method'], 0)
            method_count[line['method']] += 1
        elif line.get('message') == 'INDEX':
            method_count.setdefault('index', 0)
            method_count['index'] += 1

    print(method_count)
    stats_csv.writerow(['Videoliste angezeigt', method_count['getOrderedVideos']])
    stats_csv.writerow(['Feldliste angezeigt', method_count['getOrderedFields']])
    print('VideoListShown', method_count['getOrderedVideos'])
    print('FieldListShown', method_count['getOrderedFields'])
    print('Log lines', len(list(log_lines)))


def get_task_for_field_count(log_lines, stats_csv):
    fields = {}
    total = 0
    method_count = {}
    nvc_compliant = {True: 0, False: 0}

    for line in log_lines:
        if line.get('method') == 'getRandomTask':
            fieldId = line['args'].get('fieldId')
            if fieldId is not None:
                fieldId = int(fieldId)
            fields.setdefault(fieldId, 0)
            fields[fieldId] += 1
            total += 1

        if line.get('method') == 'getTaskAndSound':
            fieldId = line['args'].get('fieldId')
            if fieldId is not None:
                fieldId = int(fieldId)
            fields.setdefault(fieldId, 0)
            fields[fieldId] += 1
            total += 1

            nvc_compliant[line['args']['onlyNvcCompliant']] += 1


    stats_csv.writerow(['Gespielte Aufgaben', total])

    write_field_dict_to_csv('Gespielte Aufgaben pro Feld', fields, stats_csv)
    stats_csv.writerow([])

    stats_csv.writerow(['Nur GFK-konforme Stimmen?', 'Ja', nvc_compliant[True]])
    stats_csv.writerow(['', 'Nein', nvc_compliant[False]])
    stats_csv.writerow([])

    print('task for fields', format_field_dict(fields))
    print('nvc_compliant', nvc_compliant)
    print('Total tasks', total)


def get_videos_for_field_count(log_lines, stats_csv):
    fields = {}

    for line in log_lines:
        if line.get('method') == 'getVideosForField':
            fieldId = line['args'].get('fieldId')
            if fieldId is not None:
                fieldId = int(fieldId)
            fields.setdefault(fieldId, 0)
            fields[fieldId] += 1

    write_field_dict_to_csv('Hilfeseite angezeigt', fields, stats_csv)
    stats_csv.writerow([])

    print('videos for fields', format_field_dict(fields))


def get_static_text_count(log_lines, stats_csv):
    labels = {}

    for line in log_lines:
        if line.get('method') == 'getStaticText':
            label = line['args'].get('label')
            labels.setdefault(label, 0)
            labels[label] += 1

    print('getStaticText', labels)

    stats_csv.writerow(['Impressum angezeigt', labels['impressum']])
    stats_csv.writerow(['Spiel-Infos', labels['gfkspiel']])
    stats_csv.writerow(['Was ist GFK', labels['gfk']])


def get_timeline(log_lines, stats_csv):
    def write_to_file(filename, counter):
        csv_writer = csv.writer(open(filename, 'w'))
        for k, v in sorted(counter.items(), key=operator.itemgetter(0)):
            if isinstance(k, tuple):
                k = '-'.join((str(x) for x in k))
            csv_writer.writerow([k, v])


    requests_daily = Counter()
    requests_weekly = Counter()
    requests_monthly = Counter()
    requests_yearly = Counter()
    requests_weekday = Counter()
    requests_hour = Counter()

    for line in log_lines:
        if line.get('method') in ('getRandomTask', 'getTaskAndSound'):
            dt = datetime.strptime(line['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
            requests_daily[(dt.year, dt.month, dt.day)] += 1
            requests_weekly[(dt.year, dt.isocalendar()[1])] += 1
            requests_monthly[(dt.year, dt.month)] += 1
            requests_yearly[dt.year] += 1
            requests_weekday[dt.weekday()] += 1
            requests_hour[dt.hour] += 1

    write_to_file('stats/requests_daily.csv', requests_daily)
    write_to_file('stats/requests_weekly.csv', requests_weekly)
    write_to_file('stats/requests_monthly.csv', requests_monthly)
    write_to_file('stats/requests_yearly.csv', requests_yearly)
    write_to_file('stats/requests_weekday.csv', requests_weekday)
    write_to_file('stats/requests_hour.csv', requests_hour)


def get_sound_file_requests(server_log_file, stats_csv):
    total = 0
    filetypes = { 'mp3': 0, 'ogg': 0, 'undefined': 0 }
    id_to_voice = {'01': 'Klaus', '02': 'Sarina', '03': 'Antonia'}
    voices = {'Klaus': 0, 'Antonia': 0, 'Sarina': 0}
    correct = {'pos': 0, 'neg': 0}

    previous_ip_address = None
    previous_label = None
    for line in open(server_log_file):
        match = re.search('([\d\.]+) - - .*GET /audio/voice/(\w+)/([a-z]+)_(\d{2})_(\w+)', line)
        if match:
            ip_address, filetype, is_positive, voice_id, label = match.groups()

            #print(ip_address, previous_ip_address, label, previous_label)
            if ip_address == previous_ip_address and label == previous_label:
                # this seems to be a second/third 206 request for the same file from the same user
                continue

            #print(line, end='')
            previous_ip_address = ip_address
            previous_label = label

            total += 1
            filetypes[filetype] += 1
            correct[is_positive] += 1
            voices[id_to_voice[voice_id]] += 1

    stats_csv.writerow(['Korrekt geantwortet', 'Ja', correct['pos']])
    stats_csv.writerow(['', 'Nein', correct['neg']])
    stats_csv.writerow([])

    stats_csv.writerow(['Stimmen', 'Klaus', voices['Klaus']])
    stats_csv.writerow(['', 'Antonia', voices['Antonia']])
    stats_csv.writerow(['', 'Sarina', voices['Sarina']])
    stats_csv.writerow([])

    print('total', total)
    print('correct', correct)
    print('voices', voices)


def order_log_entries(log_lines, session_lifetime):
    '''
    The log file contains one line per get request or per ajax requests.

    session_lifetime: The lifetime of a session in seconds

    The return value is a list of dicts which represent a 'session'. A session
    is a series of requests from a single address. If a request is more than
    the given amount of minutes apart from the last request it will go to the
    next session.
    Each dict contains the following keys:
        addr: the ip address
        session_count: How much sessions already belong to this ip address?
        first_timestamp: The first timestamp of the current session
        last_timestamp: The last timestamp of the current session
        logs: A list of dicts. Each dict contains a request
    '''
    processed_loglines = []
    session_map = {}

    for l in log_lines:
        ts = parsets(l)
        session = None

        # Look for the most recent session
        session = session_map.get(l['remoteAddr'])
        if session:
            session['session_count'] += 1
            # Check that no more than X minutes have passed since the last timestamp
            if delta_to_seconds(session['last_timestamp'], ts) > session_lifetime:
                session = None

        if not session:
            session = {
                'addr': l['remoteAddr'],
                'session_count': 1,
                'first_timestamp': ts,
                'logs': []
            }
            processed_loglines.append(session)


        session['logs'].append(l)
        session['last_timestamp'] = ts
        session_map[session['addr']] = session
    return processed_loglines


def write_csv(filename, processed_loglines):
    ajaxmap = {
        'getStaticText': 'text',
        'getOrderedFields': 'fields',
        'getRandomTask': 'task',
        'getRandomSound': 'sound',
        'getOrderedVideos': 'video',
        'getVideosForField': 'videosForField',
        'getTaskAndSound': 'task',
        None: '',
    }

    fields = ['address', 'session_count', 'first', 'last', 'duration', 'request_count', 'requests']
    outF = open(filename, 'w')
    writer = csv.DictWriter(outF, fields)
    writer.writeheader()

    for session in processed_loglines:
        requests = []
        ignore = True
        for l in session['logs']:
            req = ajaxmap[l.get('method')] or l['message']
            if req != 'INDEX':
                ignore = False
            if req == 'getStaticText':
                req += ' (%s)' % l['args'].get('label', '')
            if req == 'videosForField':
                req += ' (%s)' % l['args'].get('fieldId', '')
            requests.append(req)

        d = {
            'address': session['addr'],
            'session_count': session['session_count'],
            'first': session['first_timestamp'].strftime('%Y-%m-%d %H:%M'),
            'last': session['last_timestamp'].strftime('%Y-%m-%d %H:%M'),
            'duration': round(delta_to_seconds(session['first_timestamp'], session['last_timestamp']) / 60., 2),
            'request_count': len(session['logs']),
            'requests': ', '.join(requests),
        }

        if not ignore:
            writer.writerow(d)

    outF.close()

lines = read_logfile(sys.argv[1])

stats_csv = csv.writer(open('stats/stats.csv', 'w'))

get_method_count(lines, stats_csv)
get_task_for_field_count(lines, stats_csv)
get_videos_for_field_count(lines, stats_csv)
get_static_text_count(lines, stats_csv)
get_timeline(lines, stats_csv)

get_sound_file_requests(sys.argv[2], stats_csv)

processed_loglines = order_log_entries(lines, 30*60)
write_csv('stats/sessions.csv', processed_loglines)
