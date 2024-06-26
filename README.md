<!--
SPDX-FileCopyrightText: Mark Thurston

SPDX-License-Identifier: Apache-2.0
-->
# Reporting templates

## Getting started

1. Clone this repository:
   `git clone https://github.com/mdvthu/report-templates && cd report-templates`
1. (optional) Create a virtual environment:
   `python3 -m venv venv && . ./venv/bin/activate`
1. Install Python dependencies
   ([Jinja2 templating](https://pypi.org/project/Jinja2/) and
   [PyYAML](https://pypi.org/project/PyYAML/)):
   `python3 -m pip install -r requirements.txt`
1. Run: `python3 build.py`: on first run this will create a config file that
   needs to be edited
1. Edit user config: `config.yaml`
1. Run: `python3 build.py`: generated templates will be in `output/text/`

## Use

### Plain text

Plain text templates will be in `output/text/`.

PowerShell can quickly copy the relevant template to the clipboard for transfer
to a report (RIS/PACS etc):

```PowerShell
Get-Content output/text/template_ct_pulmonary_angiogram.txt | Set-Clipboard
# short form
gc output/text/template_ct_pulmonary_angiogram.txt | scb
```

[Tab
completion](https://learn.microsoft.com/en-us/powershell/scripting/learn/shell/tab-completion?view=powershell-7.4)
makes this process fast.

### Voice recognition

The scripts create a `XML` file that can be imported into Dragon VR:
`output/dragon/dragon_v12.xml`

## Style

Report templates should require as few changes as possible when copying and
pasting into RIS/PACS. Whitespace can be adjusted in `templates/` directory to
customise output of the generated reports.

### Naming structure

* To keep report templates easy to navigate and remember, generated filenames
  are hierarchical.
    * `template_<modality>_<examination>_<exam_type>.txt`
    * for example, `template_mri_pelvis_contrast.txt`

### Templates for interventional procedures

* Imaging guided procedures have sufficiently different structure that they
  require a different template format. Setting `interventional: true` in the
  relevant YAML file marks the template as a procedure

## References

1. [RSNA RadReport reporting
   templates](https://www.rsna.org/practice-tools/data-tools-and-standards/radreport-reporting-templates)
1. [Radiology Assistant NL ankle
   examination](https://radiologyassistant.nl/musculoskeletal/ankle/mri-examination)
