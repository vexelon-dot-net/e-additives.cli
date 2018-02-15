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
import json
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

def ead_print_additive(additive):
  print (Fore.GREEN + 'Code')
  print (Fore.BLUE + '\tE ' + xstr(additive['code']))

  print (Fore.GREEN + 'Name')
  print (Fore.RESET + '\t' + xstr(additive['name']))

  if additive['function']:
    print (Fore.GREEN + 'Function')
    print (Fore.RESET + '\t' + additive['function'])

  if additive['notice']:
    print (Fore.GREEN + 'Warnings')
    print (Fore.RESET + '\t' + additive['notice'])

  if additive['status']:
    print (Fore.GREEN + 'Status')
    print (Fore.RESET + '\t' + additive['status'])

  if additive['foods']:
    print (Fore.GREEN + 'Foods')
    print (Fore.RESET + '\t' + additive['foods'])

  if additive['info']:
    print (Fore.GREEN + 'Details')
    print (Fore.RESET + '\t' + additive['info'])

  print (Style.RESET_ALL)

def ead_find(query):
  #TODO
  print ('FIND DUMMY')

def ead_additive(number):
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
          (SELECT value_big_text FROM ead_AdditiveProps WHERE additive_id = a.id AND key_name = 'info' AND locale_id = :locale) as info
          FROM ead_Additive AS a 
          WHERE a.code = :code""", {'code': number, 'locale': LOCALES['en']})
      conn.commit()

      data = cur.fetchone()

      if data:
        ead_print_additive(data)
      else:
        print (Style.RESET_ALL)
        print ('No results found for ' + Fore.BLUE + 'E {0}'.format(number) + Style.RESET_ALL + '!')

def ead_category(cat):
  #TODO
  print ('CATEGORY DUMMY')

def conf_get_parser():
    parser = argparse.ArgumentParser(add_help=True,
        description="So you're stuck, eh? Here're some hints.")
    parser.add_argument('query', help='search key')
    parser.add_argument('-V', '--version',
        help="""prints current version""",
        action="store_true", default=False)
    parser.add_argument('-v', '--verbose',
        help="""verbose (See what's happening)""",
        action="store_true", default=False)
    parser.add_argument('-c', '--category',
        help="""fetches additives category information""")
    parser.add_argument('-l', '--locale',
        help="""locale to display output text""")

    return parser

#############################################################################
# Main
if __name__ == "__main__":
  try:
    g_parser = conf_get_parser()
    args = g_parser.parse_args()

    g_locale = 'en'
    if args.locale:
      g_locale = g_locale if (args.locale in ['bg', 'en']) else 'en'
    
    if args.version:
      print ('{} {}'.format(os.path.basename(__file__).rstrip('.py'), VERSION))
      sys.exit(-1)
    elif args.category:
      ead_category(args.category)
    elif args.query:
      ead_additive(args.query)
    else:
      g_parser.print_help()
      sys.exit(-1)

    print (Style.RESET_ALL)

  except Exception as e:
    traceback.print_exc(file=sys.stdout)
    print ("[ERROR] {0}".format(e))