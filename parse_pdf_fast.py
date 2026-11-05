import zlib, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('references/Lumbini_Connected_Enterprise_Intelligent_Core_SAP_BTP_Strategy.pdf', 'rb') as f:
    data = f.read()

parts = data.split(b'stream')
extracted = []
for p in parts[1:]:
    end_idx = p.find(b'endstream')
    if end_idx != -1:
        s = p[:end_idx].strip()
        try:
            decomp = zlib.decompress(s)
            # find strings
            i = 0
            while True:
                start = decomp.find(b'(', i)
                if start == -1: break
                end = decomp.find(b')', start)
                if end == -1: break
                t = decomp[start+1:end].decode('utf-8', errors='ignore').strip()
                if len(t) > 2:
                    extracted.append(t)
                i = end + 1
        except:
            pass

print(f'Extracted {len(extracted)} strings.')
with open('btp_pdf_strings.txt', 'w', encoding='utf-8') as out:
    for line in extracted:
        out.write(line + '\n')
