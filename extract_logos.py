import os, zipfile

with zipfile.ZipFile('references/The_Connected_Enterprise_TEPL_Lumbini.pptx', 'r') as z:
    for name in z.namelist():
        if name.startswith('ppt/media/'):
            data = z.read(name)
            # Save to assets/extracted_logos
            os.makedirs('assets/extracted_logos', exist_ok=True)
            out_path = os.path.join('assets/extracted_logos', os.path.basename(name))
            with open(out_path, 'wb') as f:
                f.write(data)
print(f'Extracted logos from TEPL')
