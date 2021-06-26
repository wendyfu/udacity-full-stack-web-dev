# !/usr/bin/env python

import psycopg2

DB_NAME = "news"

QUERY_TOP_THREE_ARTICLES = """select a.title, count(*)
  from articles a, log l,
  (select a.id, concat('/article/', slug) as path from articles a) p
  where a.id = p.id and l.path = p.path
  group by a.title
  order by count desc
  limit 3;"""

QUERY_TOP_AUTHORS = """select au.name, count(*)
  from articles ar, authors au, log l,
  (select a.id, concat('/article/', slug) as path from articles a) p
  where ar.id = p.id and l.path = p.path and ar.author = au.id
  group by au.name
  order by count desc;"""

QUERY_ERRORS_DAYS = """select err.date,
  ((err.count::float / daily.total) * 100) from
  (select date(time),
    count(*) from log where status != '200 OK' group by date(time)) err,
  (select date(time),
    count(*) as total from log group by date(time)) daily
  where err.date = daily.date and
    ((err.count::float / daily.total) * 100) > 1;"""


def top_three_articles():
    """Return three most popular articles."""
    db = psycopg2.connect(database=DB_NAME)
    c = db.cursor()
    c.execute(QUERY_TOP_THREE_ARTICLES)
    results = c.fetchall()
    db.close()
    return results


def top_authors():
    """Return all authors sorted by page views."""
    db = psycopg2.connect(database=DB_NAME)
    c = db.cursor()
    c.execute(QUERY_TOP_AUTHORS)
    results = c.fetchall()
    db.close()
    return results


def many_errors_days():
    """Return days with more than 1% errors."""
    db = psycopg2.connect(database=DB_NAME)
    c = db.cursor()
    c.execute(QUERY_ERRORS_DAYS)
    results = c.fetchall()
    db.close()
    return results


def print_results(results, formatter):
    """Print results with the desired format.
      It's considered a best practice to return database item
      as raw as possible and do the formatting in the logical layer."""
    for item in results:
        name = item[0]
        value = item[1]
        print(formatter.format(name, value))
    print("\n")


print("=== BEGIN LOGS ANALYSIS ===\n\n")
print("1. What are the most popular three articles of all time?")
print_results(top_three_articles(), "\"{}\" - {} views")

print("2. Who are the most popular article authors of all time?")
print_results(top_authors(), "{} - {} views")

print("3. On which days did more than 1% of requests lead to errors?")
print_results(many_errors_days(), "{:%B %d, %Y} - {:.1f}% errors")
print("=== END LOGS ANALYSIS ===")
