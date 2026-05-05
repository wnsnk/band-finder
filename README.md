# band-finder
This is my first "big" project.

I build a local "website" with Flask where you can easily search for the bands or musicians without needing to look on 3 different websites.
The app can scrape the data of 3 different dutch musician classifieds.
- [Muzikantenbank.eu](https://www.muzikantenbank.eu/)
- [Muzikantenbank.net](https://www.muzikantenbank.net/)
- [Poppunt Gelderland](https://poppuntgelderland.nl/prikbord/)

Results are automatically sorted by newest.

## Installation
- clone the repository, create a virtual environment and install dependencies:
'''bash
git clone https://github.com/wnsnk/band-finder.git

cd path/to/band-finder

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
'''

- add your own environment variables to the .env file (see .env.example)

## Usage
- run the app:

```bash
python main.py
```

flask will start a local server where the app is hosted.
- in your webbrowser go to: http://127.0.0.1:5000


## Tech Stack
- Python 3.14
- Flask
- Bootstrap
- Beautiful Soup
- SQLAlchemy