# Python Text Corrector

## Installation

1) Clone the repository
```
git clone https://github.com/ground-creative/py-ai-text-corrector.git
```
2) Run the folliwng command to install dependencies
```
cd py-corrector
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3) Rename env.sample file to .env and change the content according to your needs

## Running the script

1) add the following to your crontab
```
@reboot sleep 30 && export HOME={YOUR_HOME_DIR} && export DISPLAY=:{DISPLAY_NUMBER} && {PY_CORRRECTOR_PAT}/venv/bin/python {PY_CORRRECTOR_PAT}/main.py >> {PY_CORRRECTOR_PAT}/logfile.log 2>&1
```