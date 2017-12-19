#create user 'ict-admin'@'localhost' identified by 'Az!8eeLu';
#create database ict_inventory_db;
# git remote add origin https://github.com/manuelborowski/ict-inventory.git
#git remote -v
#git push origin master
#source venv/bin/activate
#export FLASK_APP=run.py
#export FLASK_CONFIG=development
#flask run --host=0.0.0.0


xgettext -d example -o example.pot gettext_example.py
xgettext $(find . -name '*.py')

########### FIRST TIME ####################
cp example.pot to translations/nl/LC_MESSAGES/example.po
in example.po :
  change CHARSET to UTF-8
  fill in the translations
########### UPDATE ########################
cp example.pot to translations/nl/LC_MESSAGES/new.po
msgmerge -N example.po new.po > merge.po
mv merge.po example.po
in example.po :
  fill in the translations
############################################
msgfmt -o example.mo example.po

in example.py :
  t = gettext.translation('example', 'translations', fallback=True, languages=['nl'])
  t.install()
  _ = t.ugettext

  print _('This message is in the script.')


