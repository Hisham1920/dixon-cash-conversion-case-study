# Publish this project on GitHub

The public repository is https://github.com/Hisham1920/dixon-cash-conversion-case-study.

The steps below explain how to publish a separate copy if needed. For this project's existing repository, use its files and commit history.

## Website method

1. Sign in to your GitHub account.
2. Click the plus button at the top right, then **New repository**.
3. Use the name `dixon-cash-conversion-case-study`.
4. Description: `Excel financial diagnostic of Dixon Technologies with working-capital scenarios, a hypothetical collections business case, and reproducible Python analysis.`
5. Choose **Public** if you want recruiters to view it.
6. Leave the initial README option unticked because this package already contains README.md.
7. Click **Create repository**.
8. Choose the link to upload existing files.
9. Open the extracted `dixon-case-study` folder. Drag its contents into the upload area. Upload the contents, not the ZIP or an extra outer folder.
10. Commit with the message `Add Dixon financial diagnostic and operations case study`.

Check that README.md appears on the repository home page, both screenshots load, and the Excel and presentation files can be downloaded. Do not upload temporary source PDFs, internal validation output or credentials.

## Optional local calculation

In File Explorer, open the extracted project folder. Click the address bar, type `cmd` and press Enter. Then run:

```cmd
python scripts\analyse.py --check
```

Use `py` in place of `python` if your Windows installation uses the launcher. This optional command runs the independent calculations. The primary interactive model opens directly in Excel.
