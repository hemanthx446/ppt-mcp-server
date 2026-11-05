import os, zipfile

with zipfile.ZipFile('references/LumbiniEliteGroup_CompanyIntro.pptx', 'r') as z:
    for name in z.namelist():
        if name.startswith('ppt/media/'):
            os.makedirs('assets/company_logos', exist_ok=True)
            out_path = os.path.join('assets/company_logos', os.path.basename(name))
            with open(out_path, 'wb') as f:
                f.write(z.read(name))
print('Extracted all logos from CompanyIntro')
