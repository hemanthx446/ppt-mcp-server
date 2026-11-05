import re, zlib, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('references/Lumbini_Connected_Enterprise_Intelligent_Core_SAP_BTP_Strategy.pdf', 'rb') as f:
    content = f.read()

streams = re.findall(b'stream[\r\n]+(.*?)[\r\n]+endstream', content, re.DOTALL)
extracted = []
for s in streams:
    try:
        decomp = zlib.decompress(s)
        txts = re.findall(rb'\((.*?)\)', decomp)
        for t in txts:
            d = t.decode('utf-8', errors='ignore').strip()
            if len(d) > 2:
                extracted.append(d)
    except:
        pass

print(f'Total extracted pieces: {len(extracted)}')
with open('btp_extracted.txt', 'w', encoding='utf-8') as out:
    for line in extracted:
        out.write(line + '\n')
print('Wrote btp_extracted.txt')
