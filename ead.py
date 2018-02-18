#!/usr/bin/env python
# coding: utf-8
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0330

from __future__ import print_function
import os
import sys
import argparse
import traceback
import re
from time import strftime
import dateparser
import pytz
from colorama import Fore, Back, Style
import sqlite3 as lite

VERSION = '1.0'
DB_FILE = 'eadditives.sqlite3'
LOCALES = {'en': 2, 'bg': 3}

def xstr(s):
  return '' if s is None else str(s)

def xline():
  print (Fore.RESET + '-'.ljust(70, '-'))

def xkeyword(s, keyword):
  if keyword:
    pattern = re.compile('(' + keyword + ')', re.IGNORECASE)
    return pattern.sub(Fore.BLUE + r'\1' + Fore.RESET, s)
  return s

def ead_print_additive(additive, keyword=None):
  print (Style.RESET_ALL)
  print (Fore.GREEN + 'Code')
  print (Fore.BLUE + '\tE ' + xstr(additive['code']))

  print (Fore.GREEN + 'Name')
  print (Fore.RESET + '\t' + xkeyword(xstr(additive['name']), keyword))

  if additive['category']:
    print (Fore.GREEN + 'Category')
    print (Fore.RESET + '\t' + xkeyword(xstr(additive['category']), keyword))

  if additive['function']:
    print (Fore.GREEN + 'Function')
    print (Fore.RESET + '\t' + xkeyword(additive['function'], keyword))

  if additive['notice']:
    print (Fore.GREEN + 'Warnings')
    print (Fore.RESET + '\t' + xkeyword(additive['notice'], keyword))

  if additive['status']:
    print (Fore.GREEN + 'Status')
    print (Fore.RESET + '\t' + xkeyword(additive['status'], keyword))

  if additive['foods']:
    print (Fore.GREEN + 'Foods')
    print (Fore.RESET + '\t' + xkeyword(additive['foods'], keyword))

  if additive['info']:
    print (Fore.GREEN + 'Details')
    print (Fore.RESET + '\t' + xkeyword(additive['info'], keyword))

  print (Style.RESET_ALL)

def ead_print_category(category):
  print (Style.RESET_ALL)
  print (Fore.GREEN + 'Name')
  print (Fore.RESET + '\t' + xstr(category['name']))

  if category['description']:
    print (Fore.GREEN + 'Description')
    print (Fore.RESET + '\t' + category['description'])

  if category['additives']:
    print (Fore.GREEN + 'Additives in database')
    print (Fore.RESET + '\t' + xstr(category['additives']))

  print (Style.RESET_ALL)

def ead_search(query, locale):
  conn = lite.connect(DB_FILE)
  with conn:
    conn.row_factory = lite.Row

    cur = conn.cursor()
    cur.execute("""SELECT a.id, a.code,
        (SELECT value_str FROM ead_AdditiveProps WHERE additive_id = a.id AND key_name = 'name' AND locale_id = :locale) as name,
        (SELECT value_text FROM ead_AdditiveProps WHERE additive_id = a.id AND key_name = 'status' AND locale_id = :locale) as status,
        (SELECT value_str FROM ead_AdditiveProps WHERE additive_id = a.id AND key_name = 'veg' AND locale_id = :locale) as veg,
        (SELECT value_text FROM ead_AdditiveProps WHERE additive_id = a.id AND key_name = 'function' AND locale_id = :locale) as function,
        (SELECT value_text FROM ead_AdditiveProps WHERE additive_id = a.id AND key_name = 'foods' AND locale_id = :locale) as foods,
        (SELECT value_text FROM ead_AdditiveProps WHERE additive_id = a.id AND key_name = 'notice' AND locale_id = :locale) as notice,
        (SELECT value_big_text FROM ead_AdditiveProps WHERE additive_id = a.id AND key_name = 'info' AND locale_id = :locale) as info,
        (SELECT name FROM ead_AdditiveCategoryProps WHERE category_id = a.category_id AND locale_id = :locale) as category
        FROM ead_Additive AS a 
        WHERE name LIKE :query 
          OR status LIKE :query 
          OR function LIKE :query 
          OR foods LIKE :query 
          OR notice LIKE :query 
          OR info LIKE :query""", 
        {'query': ('%{}%').format(query.lower()), 'locale': locale})
    conn.commit()

    results = cur.fetchall()

    if results:
      print ('\nHere is what I found:')
      for additive in results:
        xline()
        ead_print_additive(additive, query)
      xline()
    else:
      print (Style.RESET_ALL)
      print ('No results found for ' + Fore.BLUE + '{0}'.format(query) + Style.RESET_ALL + '!')

def ead_additive(number, locale):
  conn = lite.connect(DB_FILE)
  with conn:
    conn.row_factory = lite.Row

    cur = conn.cursor()
    cur.execute("""SELECT a.id, a.code, a.last_update, a.category_id,
        (SELECT value_str FROM ead_AdditiveProps WHERE additive_id = a.id AND key_name = 'name' AND locale_id = :locale) as name,
        (SELECT value_text FROM ead_AdditiveProps WHERE additive_id = a.id AND key_name = 'status' AND locale_id = :locale) as status,
        (SELECT value_str FROM ead_AdditiveProps WHERE additive_id = a.id AND key_name = 'veg' AND locale_id = :locale) as veg,
        (SELECT value_text FROM ead_AdditiveProps WHERE additive_id = a.id AND key_name = 'function' AND locale_id = :locale) as function,
        (SELECT value_text FROM ead_AdditiveProps WHERE additive_id = a.id AND key_name = 'foods' AND locale_id = :locale) as foods,
        (SELECT value_text FROM ead_AdditiveProps WHERE additive_id = a.id AND key_name = 'notice' AND locale_id = :locale) as notice,
        (SELECT value_big_text FROM ead_AdditiveProps WHERE additive_id = a.id AND key_name = 'info' AND locale_id = :locale) as info,
        (SELECT name FROM ead_AdditiveCategoryProps WHERE category_id = a.category_id AND locale_id = :locale) as category
        FROM ead_Additive AS a 
        WHERE a.code = :code""", {'code': number, 'locale': locale})
    conn.commit()

    results = cur.fetchone()

    if results:
      ead_print_additive(results)
    else:
      print (Style.RESET_ALL)
      print ('No results found for ' + Fore.BLUE + 'E {0}'.format(number) + Style.RESET_ALL + '!')

def ead_category(cat, locale):
  conn = lite.connect(DB_FILE)
  with conn:
    conn.row_factory = lite.Row

    cur = conn.cursor()

    if cat and cat.lower() != 'all':
      cur.execute("""SELECT c.id, p.name, p.description, p.last_update,
            (SELECT COUNT(id) FROM ead_Additive as a WHERE a.category_id=c.id) as additives
            FROM ead_AdditiveCategory as c
            LEFT JOIN ead_AdditiveCategoryProps as p ON p.category_id = c.id
            WHERE p.name LIKE :category AND p.locale_id = :locale""", 
            {'category': ('%{}%').format(cat.lower()), 'locale': locale})
    else:
      cur.execute("""SELECT c.id, p.name, p.description, p.last_update,
            (SELECT COUNT(id) FROM ead_Additive as a WHERE a.category_id=c.id) as additives
            FROM ead_AdditiveCategory as c
            LEFT JOIN ead_AdditiveCategoryProps as p ON p.category_id = c.id
            WHERE p.locale_id = :locale""", {'locale': locale})

    conn.commit()
    results = cur.fetchall()

    if results:
      print ('\nHere is what I found:')
      for cat in results:
        xline()
        ead_print_category(cat)
      xline()
    else:
      print (Style.RESET_ALL)
      print ('No results found for category ' + Fore.BLUE + 
        '{0}'.format(cat) + Style.RESET_ALL + '!')

def conf_get_parser():
  parser = argparse.ArgumentParser(add_help=True,
      description="So you're stuck, eh? Here are some hints.")
  parser.add_argument('query', help='E number or search phrase', nargs='?')
  parser.add_argument('-c', '--category',
      help="""fetches additives category information. Specify 'all' to fetch
      infos for all categories or query by name; e.g. colors, antibiotics, etc.""",
      action="store_true", default=False)
  parser.add_argument('-l', '--locale',
      help="""locale to display output text""", default='en')
  parser.add_argument('-V', '--version',
      help="""prints current version""",
      action="store_true", default=False)

  return parser

#############################################################################
# Main
if __name__ == "__main__":
  try:
    parser = conf_get_parser()
    args = parser.parse_args()

    locale = LOCALES[args.locale if (args.locale in ['bg', 'en']) else 'en']
    
    if args.version:
      print ('{} {}'.format(os.path.basename(__file__).rstrip('.py'), VERSION))
      sys.exit(-1)
    elif args.category:
      ead_category(args.query, locale=locale)
    elif args.query:
      re_additive = re.compile('^\d{3,4}$')
      if re_additive.match(args.query):
        ead_additive(args.query, locale=locale)
      else:
        ead_search(args.query, locale=locale)
    else:
      parser.print_help()
      sys.exit(-1)

    print (Style.RESET_ALL)

  except Exception as e:
    traceback.print_exc(file=sys.stdout)
    print ("[ERROR] {0}".format(e))