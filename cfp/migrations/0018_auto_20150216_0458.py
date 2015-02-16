# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0017_auto_20150216_0347'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=60),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(default='US', max_length=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conference',
            name='programming_language',
            field=models.CharField(default='', blank=True, choices=[('', ''), ('.NET', '.NET'), ('Actionscript', 'Actionscript'), ('Ada', 'Ada'), ('Agda', 'Agda'), ('Android', 'Android'), ('AppceleratorTitanium', 'AppceleratorTitanium'), ('Autotools', 'Autotools'), ('C', 'C'), ('C++', 'C++'), ('C#', 'C#'), ('CakePHP', 'CakePHP'), ('Chef', 'Chef'), ('Clojure', 'Clojure'), ('CodeIgniter', 'CodeIgniter'), ('CommonLisp', 'CommonLisp'), ('Composer', 'Composer'), ('Dart', 'Dart'), ('Delphi', 'Delphi'), ('Drupal', 'Drupal'), ('Elisp', 'Elisp'), ('Elixir', 'Elixir'), ('Erlang', 'Erlang'), ('F#', 'F#'), ('ForceDotCom', 'ForceDotCom'), ('Fortran', 'Fortran'), ('GWT', 'GWT'), ('Go', 'Go'), ('Gradle', 'Gradle'), ('Grails', 'Grails'), ('Haskell', 'Haskell'), ('Idris', 'Idris'), ('Java', 'Java'), ('Javascript', 'Javascript'), ('Jboss', 'Jboss'), ('Jekyll', 'Jekyll'), ('Joomla', 'Joomla'), ('Laravel', 'Laravel'), ('Leiningen', 'Leiningen'), ('Lithium', 'Lithium'), ('Magento', 'Magento'), ('Maven', 'Maven'), ('Mercury', 'Mercury'), ('Meteor', 'Meteor'), ('Node', 'Node'), ('OCaml', 'OCaml'), ('Objective-C', 'Objective-C'), ('Opa', 'Opa'), ('Packer', 'Packer'), ('Perl', 'Perl'), ('PHP', 'PHP'), ('Phalcon', 'Phalcon'), ('PlayFramework', 'PlayFramework'), ('Plone', 'Plone'), ('Processing', 'Processing'), ('Puppet', 'Puppet'), ('Python', 'Python'), ('Qooxdoo', 'Qooxdoo'), ('Qt', 'Qt'), ('R', 'R'), ('Rails', 'Rails'), ('Ruby', 'Ruby'), ('Rust', 'Rust'), ('Sass', 'Sass'), ('Scala', 'Scala'), ('Scrivener', 'Scrivener'), ('SketchUp', 'SketchUp'), ('SugarCRM', 'SugarCRM'), ('Swift', 'Swift'), ('Symfony', 'Symfony'), ('TeX', 'TeX'), ('Unity', 'Unity'), ('VisualStudio', 'VisualStudio'), ('Waf', 'Waf'), ('WordPress', 'WordPress'), ('Yeoman', 'Yeoman'), ('Yii', 'Yii'), ('ZendFramework', 'ZendFramework'), ('Zephir', 'Zephir')], max_length=30, db_index=True),
            preserve_default=True,
        ),
    ]
