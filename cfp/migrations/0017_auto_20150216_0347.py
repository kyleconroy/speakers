# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0016_conference_programming_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 2, 16, 3, 47, 24, 688982, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talk',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 2, 16, 3, 47, 28, 488807, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='conference',
            name='programming_language',
            field=models.CharField(db_index=True, max_length=30, default='', choices=[('', ''), ('.NET', '.NET'), ('Actionscript', 'Actionscript'), ('Ada', 'Ada'), ('Agda', 'Agda'), ('Android', 'Android'), ('AppceleratorTitanium', 'AppceleratorTitanium'), ('Autotools', 'Autotools'), ('C', 'C'), ('C++', 'C++'), ('C#', 'C#'), ('CakePHP', 'CakePHP'), ('Chef', 'Chef'), ('Clojure', 'Clojure'), ('CodeIgniter', 'CodeIgniter'), ('CommonLisp', 'CommonLisp'), ('Composer', 'Composer'), ('Dart', 'Dart'), ('Delphi', 'Delphi'), ('Drupal', 'Drupal'), ('Elisp', 'Elisp'), ('Elixir', 'Elixir'), ('Erlang', 'Erlang'), ('F#', 'F#'), ('ForceDotCom', 'ForceDotCom'), ('Fortran', 'Fortran'), ('GWT', 'GWT'), ('Go', 'Go'), ('Gradle', 'Gradle'), ('Grails', 'Grails'), ('Haskell', 'Haskell'), ('Idris', 'Idris'), ('Java', 'Java'), ('Javascript', 'Javascript'), ('Jboss', 'Jboss'), ('Jekyll', 'Jekyll'), ('Joomla', 'Joomla'), ('Laravel', 'Laravel'), ('Leiningen', 'Leiningen'), ('Lithium', 'Lithium'), ('Magento', 'Magento'), ('Maven', 'Maven'), ('Mercury', 'Mercury'), ('Meteor', 'Meteor'), ('Node', 'Node'), ('OCaml', 'OCaml'), ('Objective-C', 'Objective-C'), ('Opa', 'Opa'), ('Packer', 'Packer'), ('Perl', 'Perl'), ('PHP', 'PHP'), ('Phalcon', 'Phalcon'), ('PlayFramework', 'PlayFramework'), ('Plone', 'Plone'), ('Processing', 'Processing'), ('Puppet', 'Puppet'), ('Python', 'Python'), ('Qooxdoo', 'Qooxdoo'), ('Qt', 'Qt'), ('R', 'R'), ('Rails', 'Rails'), ('Ruby', 'Ruby'), ('Rust', 'Rust'), ('Sass', 'Sass'), ('Scala', 'Scala'), ('Scrivener', 'Scrivener'), ('SketchUp', 'SketchUp'), ('SugarCRM', 'SugarCRM'), ('Swift', 'Swift'), ('Symfony', 'Symfony'), ('TeX', 'TeX'), ('Unity', 'Unity'), ('VisualStudio', 'VisualStudio'), ('Waf', 'Waf'), ('WordPress', 'WordPress'), ('Yeoman', 'Yeoman'), ('Yii', 'Yii'), ('ZendFramework', 'ZendFramework'), ('Zephir', 'Zephir')]),
            preserve_default=True,
        ),
    ]
