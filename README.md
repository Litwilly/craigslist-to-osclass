# craigslist-to-osclass
Import craigslist ads to opensource classified framework osclass using python and osclass plugin Ad Importer https://market.osclass.org/plugins/ad-management/ad-importer_53.

Requires providing a CSV file of desired listings to add, will also dig up reply email address.

## Dependencies
- BautifulSoup

## Files
- **xmlMaker.py** - python script that builds the XML file used by "Ad Importer" plugin

- **urls.csv** - CSV file used by xmlMaker.py
  - Column A - Listing URL
  - Column B - Category *#must match your category spelling or a new category will be created*
  - Column C - City *#will use craigslist region if nothing is present*
  - Column D - Region *#I use Region as State in my osclass*
  - Column E - Custom Fields
  - Column F - Phone Number *#Appended after content*
  
- **craigslist.xml** - XML file create by xmlMaker.py
