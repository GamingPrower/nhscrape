# nhscrape
nhentai scraper! Search results, Popular results, Book pages, Everything!

Originally a beginner learning project turned into a mission. I made an unfinished nodejs version of this scraper a couple weeks ago
and stopped working on it when I found out they had an API. Welp they discontinued it so this is what I made.

This is literally my first project in Python so hopefully its not of poor quality. Let me know how I can improve if you feel like it!

```
from nhscrape import FrontPage, SearchResults, BookResults
```

```
FrontPage.get()
```
Returns the front page results in the form of an object(Titles, Cover Images, URLs)

```
SearchResults.get(query, page=1, popular=False)
```
Returns search results for a specified page(defaults to 1) and displays the Popular section if specified as "True"
Like FrontPage.get() this method returns Titles, Cover Images, and URLS

```
BookResults.get(link OR id)
```
For those who want to scrape the actually book pages, this is for you. Returns ALL of the lowres and highres versions of each page.

```
BookResults.getInfoFromBook(link OR id)
```
This provides the book information found at the top of the page. Returns list of tags, cover image, and book title.
Unfortunately I wasn't able to retrieve artist name here which is a shame, would love to figure out how to do that.
