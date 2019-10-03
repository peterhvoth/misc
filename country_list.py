from iso3166 import countries
import re

for country in countries:
    print(re.sub('\W', '', country.name).lower())