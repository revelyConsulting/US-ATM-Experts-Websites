import json, os, subprocess, sys, glob
PAL=json.load(open('states/palettes.json'))
CANNABIS={"CA","CO","WA","OR","NV","NM","MI","IL","MA","ME","VT","NJ","NY","CT","RI","DE","MD","VA","MO","OH","MN","MT","AK","HI","OK","AR","FL","PA","LA","MS","WV","KY","UT","ND","SD","NH"}
only=sys.argv[1:] 
for f in sorted(glob.glob('states/[A-Z][A-Z].json')):
    d=json.load(open(f)); ab=d["abbr"]
    if only and ab not in only: continue
    d["palette"]=PAL[ab]; d["cannabis"]=ab in CANNABIS
    cfg=f'states/cfg_{ab}.json'; json.dump(d,open(cfg,'w'))
    out=f'multistate/{ab.lower()}atmexperts.com'
    os.makedirs(out,exist_ok=True)
    r=subprocess.run(['python3','build_state.py',cfg,out],capture_output=True,text=True)
    print(ab, r.stdout.strip() or r.stderr.strip()[-400:])
