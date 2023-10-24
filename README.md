# Unoffical BART API

BART API that scrapes data from bart.gov, created because the BART Legacy API is unstable.

## Issues with the legacy API
BART's legacy API is the RESTful API provided by BART. Sadly, it doesn't work well. The errors provided by the server are non-descriptive (all errors say "invalid API key", even when that is not the case), and the API will unexplainably stop working. The natural solution for me was to scrape information from BART's website. This project aims to be a stand-in replacement for the API, however, it shouldn't be used in product as at any time, BART could pull the plug and block my IP, or Cloudflare could randomly start blocking me.

## Feedback
If you have any feedback, concerns, or suggestions, please contact me using me@trentwil.es. Additionally, you should submit pull requests if you see something that should be changed or repaired!