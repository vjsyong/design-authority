#!/usr/bin/env python3
"""Cadence fixture v3 — explicit skip-sets (full control) + seeded minute jitter."""
import json, datetime as dt

M = 0xFFFFFFFF
def mulberry32(a):
    while True:
        a = (a + 0x6D2B79F5) & M
        t = (a ^ (a >> 15)) * (a | 1) & M
        t = (t + (((t ^ (t >> 7)) * (t | 61)) & M)) & M
        t = (t ^ (t >> 14)) & M
        yield t / 4294967296.0

RITUALS = [
    dict(id='r1', name='Morning stretch', cat='Body',  freq='daily',    mins=10),
    dict(id='r2', name='Read 20 pages',  cat='Mind',  freq='daily',    mins=20),
    dict(id='r3', name='Evening walk',   cat='Body',  freq='weekdays', mins=30),
    dict(id='r4', name='Journal',        cat='Mind',  freq='daily',    mins=15),
    dict(id='r5', name='Piano practice', cat='Craft', freq='weekends', mins=25),
]
SKIPS = {
 'r1': {'2026-09-06','2026-09-10','2026-09-18','2026-10-04'},
 'r2': {'2026-09-04','2026-09-07','2026-09-15','2026-09-23','2026-09-29','2026-10-05'},
 'r3': {'2026-09-08','2026-09-16','2026-09-24','2026-10-01'},
 'r4': {'2026-09-04','2026-09-09','2026-09-11','2026-09-21','2026-09-27','2026-10-03'},
 'r5': {'2026-09-05','2026-09-12','2026-09-19','2026-10-03','2026-10-04'},
}
BREAKS = {'2026-09-25','2026-09-20','2026-09-14'}
TODAY = dt.date(2026, 10, 7)
START = TODAY - dt.timedelta(days=34)

def applicable(r, d):
    if r['freq'] == 'daily': return True
    if r['freq'] == 'weekdays': return d.weekday() < 5
    return d.weekday() >= 5

rng = mulberry32(20261007)
nxt = lambda: next(rng)

logs = {}
d = START
while d <= TODAY:
    key = d.isoformat()
    day = {}
    if key not in BREAKS:
        for r in RITUALS:
            if not applicable(r, d) or key in SKIPS[r['id']]:
                continue
            if key == '2026-10-07':
                day[r['id']] = 12 if r['id'] == 'r1' else 25 if r['id'] == 'r2' else r['mins']
                if r['id'] not in ('r1', 'r2'):
                    del day[r['id']]
                continue
            day[r['id']] = r['mins'] + int(nxt() * 6)
    if day:
        logs[key] = day
    d += dt.timedelta(days=1)

def dstr(x): return x.isoformat()
streak = 0
d = TODAY
while dstr(d) in logs:
    streak += 1; d -= dt.timedelta(days=1)

week = [dt.date(2026,10,5) + dt.timedelta(days=i) for i in range(7)]
week_sums = [sum(logs.get(dstr(x), {}).values()) for x in week]
last7 = [TODAY - dt.timedelta(days=i) for i in range(6, -1, -1)]
last7_sums = [sum(logs.get(dstr(x), {}).values()) for x in last7]
total_logs = sum(len(v) for v in logs.values())
total_mins = sum(sum(v.values()) for v in logs.values())

print('days with logs:', len(logs), '/ 35')
print('streak:', streak)
print('week sums Mon..Sun:', week_sums, '| Wed(today) =', week_sums[2])
print('last7 sums (Sep30..Oct6):', last7_sums)
print('total logs:', total_logs, 'total mins:', total_mins)
print('today:', logs.get('2026-10-07'))
for r in RITUALS:
    sched = [x for x in last7[:-1] if applicable(r, x)]
    missed = [x for x in sched if r['id'] not in logs.get(dstr(x), {})]
    print(f"  {r['id']}: scheduled {len(sched)} missed {len(missed)} -> {'SLIPPING' if len(missed)>=2 else 'ON TRACK'} | last logged {max([dstr(x) for x in last7+last7 if r['id'] in logs.get(dstr(x), {})], default='—')}")

out = {'today': '2026-10-07', 'week_start': '2026-10-05', 'logs': {k: logs[k] for k in sorted(logs)}}
open('/home/xrim/.hermes/cache/scratch/cadence3_fixture.json', 'w').write(json.dumps(out, indent=1))
print('wrote /home/xrim/.hermes/cache/scratch/cadence3_fixture.json bytes:', len(json.dumps(out)))
