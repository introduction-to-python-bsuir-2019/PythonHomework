# euseand's RSS-reader
My RSS-reader is a command line utility which parses RSS URL and prints news in human-readable format.
## installation
You can use pip to install my package from test pypi index:
```bash
pip install --extra-index-url https://test.pypi.org/simple/ rss-reader-euseand==0.420
```
Or simply clone the repo and use pip install:
```bash
git clone --branch FinalTask https://github.com/euseand/PythonHomework.git
pip install .
``` 
## usage
Print 10(default limit) news from default (yahoo) online feed:
```bash
rss-reader ""
```
Print 10 news from online feed and store it in HTML-page (with additional verbosity):
```bash
rss-reader "https://news.yahoo.com/rss/" --limit 10 --verbose --to-html
```
Print 10 news from online feed and store it in PDF-file (with additional verbosity):
```bash
rss-reader "https://news.yahoo.com/rss/" --limit 10 --verbose --to-pdf
```
Print 10 news from cached feed and store it in HTML-page:
```bash
rss-reader "https://news.yahoo.com/rss/" --limit 10 --date 20191129
```
## feed examples (tested):
```bash
https://news.google.com/news/rss
https://news.yahoo.com/rss/
```
## JSON structure:
```
{
 "news": [
  {
   "feed": "Yahoo News - Latest News & Headlines",
   "url": "https://news.yahoo.com/rss/",
   "news_objects": [
    {
     "title": "Germany to make anti-Semitism a specific hate crime as Jews 'no longer feel safe'",
     "date": "Fri, 29 Nov 2019 12:02:48 -0500",
     "url": "https://news.yahoo.com/germany-crack-down-anti-semitic-170248885.html",
     "description": "Germany is to tighten its laws against anti-Semitic hate crimes\u00a0in the wake of last month's\u00a0failed attack on a synagogue by a far-Right gunman.
 \u201cI am ashamed that Jews no longer feel safe in Germany and that so many are even thinking of leaving the country,\u201d Christine Lambrecht, the justice minister, told
German MPs. \u201cWe have to send a clear signal against anti-Semitism.\u201d Under the planned changes, crimes with an anti-Semitic motive will attract heavier sentences. Th
e move comes after a synagogue in east Germany narrowly escaped becoming the scene of a massacre last month. Stephan Balliet, a German national who released a far-Right \"man
ifesto\" before the attack, failed in his attempts to break into the synagogue\u00a0which was packed with 51\u00a0 people marking Yom Kippur, the holiest day of the Jewish ca
lendar. He later turned his gun on bystanders, killing two people. While the Halle attack was the highest profile incident, it was by no means an isolated case. Just days bef
ore, a Syrian man was stopped by security guards as he tried to enter Berlin\u2019s best known synagogue armed with a knife and shouting \u201cAllahu akbar\u201d and \u201cF*
** Israel\u201d. Anti-Semitic crimes across Germany rose by 10 per cent to a total of 1,646 last year, but it is the figures for violence that are most alarming. Violent anti
-Semitic crimes rose by 60 per cent, with 62 offences leaving 43 people injured. More than 50 people were trapped inside the synagogue while the gunman tried to gain entry Cr
edit: Craig Stennett for the Telegraph They include the case of an Israeli man who was attacked and whipped with a belt while wearing a Jewish kippah skullcap in central Berl
in in April last year. Adam Armoush, an Israeli Arab who lives in Berlin, is not Jewish but was wearing the kippah in an attempt to prove Berlin was safe for Jewish people. I
n the wake of that incident felix Klein, the German government\u2019s anti-Semitism commissioner,\u00a0issued a warning to Jewish men not to wear skullcaps in public for thei
r own safety. Mr Klein later retracted his warning after a public outcry. In another case in July last year, a Jewish Syrian man wearing a Star of David pendant was attacked
and beaten by a group of people when he stopped to ask for a light for his cigarette in central Berlin. Anti-Semitic incidents last year also include one an attack on a Jewis
h restaurant in the east German city of Chemnitz. Masked men broke surrounded the entrance to the restaurant and broke the windows with stones while the owner was trapped ins
ide. Current German laws recognise discrimination against a particular group of people as an aggravating factor in any crime that can lead to a heavier sentence. But the plan
ned changes will explicitly name anti-Semitism for the first time. The change is part of a package introduced after the Halle synagogue attack. Other measures include laws ob
liging social media networks to inform the authorities of online threats and incitement to hatred. \u201cThis is an important step towards consistent punishment of anti-Semit
ic crimes,\u201d said Josef Schuster, head of the Central Council of Jews in Germany. \u201cWith the planned amendment to the law, the federal government is living up to its
commitment to fight anti-Semitism resolutely and protect Jewish life.\u201d \u201cAnti-Semitic offences are not just attacks on individual people of the Jewish faith, they al
ways an attack on our values, on our constitutional state, and on our democracy as a whole,\u201d said Georg Eisenreich, the regional justice minister for Bavaria, where pros
ecutors recently announced they will prioritise anti-Semitic crimes.",
     "links": [
      {
       "id": 0,
       "url": "https://news.yahoo.com/germany-crack-down-anti-semitic-170248885.html",
       "type": "link"
      },
      {
       "id": 1,
       "url": "http://l2.yimg.com/uu/api/res/1.2/bqRbLeY6nn2Uvt9BhPAhSg--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media.zenfs.com/en-GB/the_telegraph_258/624e2d0a809f39d
27baa4175783c060f",
       "type": "image",
       "alt": "Germany to make anti-Semitism a specific hate crime as Jews 'no longer feel safe'"
      }
     ]
    }
   ]
  },
  {
   "feed": "Top stories - Google News",
   "url": "https://news.google.com/news/rss",
   "news_objects": [
    {
     "title": "House Intelligence Committee to vote on impeachment report - NBC News",
     "date": "Sun, 01 Dec 2019 05:42:00 GMT",
     "url": "https://news.google.com/__i/rss/rd/articles/CBMieGh0dHBzOi8vd3d3Lm5iY25ld3MuY29tL3BvbGl0aWNzL3RydW1wLWltcGVhY2htZW50LWlucXVpcnkvaG91c2UtaW50ZWxsaWdlbmNlLWNvbW1pd
HRlZS12b3RlLWltcGVhY2htZW50LXJlcG9ydC1uMTA5MzcwMdIBLGh0dHBzOi8vd3d3Lm5iY25ld3MuY29tL25ld3MvYW1wL25jbmExMDkzNzAx?oc=5",
     "description": "House Intelligence Committee to vote on impeachment report\u00a0\u00a0NBC NewsHouse Democrats charge ahead with next phase of impeachment proceedings\u00
a0\u00a0CBS Evening NewsPresidential historian predicts public support for Trump will collapse | TheHill\u00a0\u00a0The HillWhat swimming in my underwear taught me about Dona
ld Trump and getting away with it\u00a0\u00a0USA TODAYThe Politics of Impeachment\u00a0\u00a0The New York TimesView full coverage on Google News",
     "links": [
      {
       "id": 0,
       "url": "https://news.google.com/__i/rss/rd/articles/CBMieGh0dHBzOi8vd3d3Lm5iY25ld3MuY29tL3BvbGl0aWNzL3RydW1wLWltcGVhY2htZW50LWlucXVpcnkvaG91c2UtaW50ZWxsaWdlbmNlLWNvbW1
pdHRlZS12b3RlLWltcGVhY2htZW50LXJlcG9ydC1uMTA5MzcwMdIBLGh0dHBzOi8vd3d3Lm5iY25ld3MuY29tL25ld3MvYW1wL25jbmExMDkzNzAx?oc=5",
       "type": "link"
      },
      {
       "id": 1,
       "url": "https://news.google.com/__i/rss/rd/articles/CBMiK2h0dHBzOi8vd3d3LnlvdXR1YmUuY29tL3dhdGNoP3Y9X2J0Z2E3T0N1NWvSAQA?oc=5",
       "type": "link"
      },
      {
       "id": 2,
       "url": "https://news.google.com/__i/rss/rd/articles/CBMia2h0dHBzOi8vdGhlaGlsbC5jb20vbWVkaWEvNDcyNDU4LWNubi1wcmVzaWRlbnRpYWwtaGlzdG9yaWFuLXByZWRpY3RzLXB1YmxpYy1zdXBwb3J
0LWZvci10cnVtcC13aWxsLWNvbGxhcHNl0gFvaHR0cHM6Ly90aGVoaWxsLmNvbS9tZWRpYS80NzI0NTgtY25uLXByZXNpZGVudGlhbC1oaXN0b3JpYW4tcHJlZGljdHMtcHVibGljLXN1cHBvcnQtZm9yLXRydW1wLXdpbGwtY29sb
GFwc2U_YW1w?oc=5",
       "type": "link"
      },
      {
       "id": 3,
       "url": "https://news.google.com/__i/rss/rd/articles/CBMigQFodHRwczovL3d3dy51c2F0b2RheS5jb20vc3Rvcnkvb3Bpbmlvbi8yMDE5LzEyLzAxL2ltcGVhY2htZW50LWhpc3RvcmljLXZpdGFsLXN0YXR
lbWVudC10cmFnaWMtdHJ1bXAtcHJlc2lkZW5jeS1jb2x1bW4vNDMxMTUyMTAwMi_SASdodHRwczovL2FtcC51c2F0b2RheS5jb20vYW1wLzQzMTE1MjEwMDI?oc=5",
       "type": "link"
      },
      {
       "id": 4,
       "url": "https://news.google.com/__i/rss/rd/articles/CBMiSWh0dHBzOi8vd3d3Lm55dGltZXMuY29tLzIwMTkvMTEvMzAvb3Bpbmlvbi9sZXR0ZXJzL3RydW1wLWltcGVhY2htZW50Lmh0bWzSAU1odHRwczo
vL3d3dy5ueXRpbWVzLmNvbS8yMDE5LzExLzMwL29waW5pb24vbGV0dGVycy90cnVtcC1pbXBlYWNobWVudC5hbXAuaHRtbA?oc=5",
       "type": "link"
      },
      {
       "id": 5,
       "url": "https://news.google.com/stories/CAAqOQgKIjNDQklTSURvSmMzUnZjbmt0TXpZd1NoTUtFUWpHanRuQWpvQU1FUnA2NWZhQnNwQ1FLQUFQAQ?oc=5",
       "type": "link"
      }
     ]
    },    
   ]
  }
 ]
}

```