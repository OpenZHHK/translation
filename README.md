# OpenZHHK App

Build by [Ankur Singh](ankur13019@iiitd.ac.in) for freelancer user josephlam.

## Tech Specs

- Python 2.7.11
- Flask
- Flask-Restful
- Flask-mongoengine
- WTForms

## Installation

- Install python ([Anaconda](https://www.continuum.io/anaconda) preferred) 

## Models

Only one model - Word

Fields:

- input:string:required
- translation:string:required
- frequency:integer>=0:default=0
- flags:string
- originalip:string
- lastip:string
- deleted:boolean:default=false
- singleword:boolean:default=dynamicially_computed
- created_at:datetime (from timestamps!)
- updated_at:datetime (from timestamps!)

## REST API

### /api/v1/word

> GET /?page=1&count=5: Index ordered by frequency, paginated by page and items = count
> POST /: Create from params[word]
> GET /id: Show
> POST /id: Update
> DELETE /id: Delete

> GET /download?type=(single|multiple): get all words, of the type defined sorted by name in the given format
> POST /upload: upload a file with the a delimited file to create word objects in bulk

## Delimited File Format

```
openzhhk.com,dictionary=main:en,locale=en,description=zhhk,date=20160224,version=47 
input=bonjour,translation=hello,frequency=222,flags=greeting
input=archi,translation=bye,frequency=212,flags=greeting
input=dimi,translation=work,frequency=192,flags=
input=coupe,translation=love,frequency=102,flags=
input=aubau,translation=food,frequency=34,flags=

date = (date of the generation of the delimited file)
version = (this value is a number present in version.txt)
The make the delimited file more compact, we might want to think about using the following abbreviations:
input = i
translation = t
frequency = f
flags = ff

So the first line would be:
i=dimi,t=work,f=192,ff=
```

## Routes

> GET /: The search page
- Display a message if not found
> GET /new: The new page (the online form) (with the upload button)
- No Duplicate Entries
- Defination of unique: (input,translation) is unique
> GET /list?: Show all the entries, paginated with infinite scroll/lazy load ajax
- Option type: single/multiple word support
- Option q: string to search
- Show the q and type settings on the top of the page
- Download button for all (use the same settings) (Use two buttons search and download)
- Show as a simple bootstrap table, with check box and a delete button on top to delete selected after confirmation
> GET /stats: Show the stats 
- Entries in the database
- Latest Updation date time
- Unique inputs
- Unique translations
- Unique IPs



