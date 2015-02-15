# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0015_auto_20150214_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='programming_language',
            field=models.CharField(default='', choices=[('', ''), ('Actionscript', 'Actionscript'), ('Ada', 'Ada'), ('Agda', 'Agda'), ('Android', 'Android'), ('AppceleratorTitanium', 'AppceleratorTitanium'), ('ArchLinuxPackages', 'ArchLinuxPackages'), ('Autotools', 'Autotools'), ('Bancha', 'Bancha'), ('C', 'C'), ('C++', 'C++'), ('CFWheels', 'CFWheels'), ('CMake', 'CMake'), ('CakePHP', 'CakePHP'), ('ChefCookbook', 'ChefCookbook'), ('Clojure', 'Clojure'), ('CodeIgniter', 'CodeIgniter'), ('CommonLisp', 'CommonLisp'), ('Composer', 'Composer'), ('Concrete5', 'Concrete5'), ('Coq', 'Coq'), ('CraftCMS', 'CraftCMS'), ('DM', 'DM'), ('Dart', 'Dart'), ('Delphi', 'Delphi'), ('Drupal', 'Drupal'), ('EPiServer', 'EPiServer'), ('Eagle', 'Eagle'), ('Elisp', 'Elisp'), ('Elixir', 'Elixir'), ('Erlang', 'Erlang'), ('ExpressionEngine', 'ExpressionEngine'), ('ExtJS-MVC', 'ExtJS-MVC'), ('Fancy', 'Fancy'), ('Finale', 'Finale'), ('ForceDotCom', 'ForceDotCom'), ('Fortran', 'Fortran'), ('FuelPHP', 'FuelPHP'), ('GWT', 'GWT'), ('GitBook', 'GitBook'), ('Go', 'Go'), ('Gradle', 'Gradle'), ('Grails', 'Grails'), ('Haskell', 'Haskell'), ('Idris', 'Idris'), ('Java', 'Java'), ('Jboss', 'Jboss'), ('Jekyll', 'Jekyll'), ('Joomla', 'Joomla'), ('Jython', 'Jython'), ('Kohana', 'Kohana'), ('LabVIEW', 'LabVIEW'), ('Laravel', 'Laravel'), ('Leiningen', 'Leiningen'), ('LemonStand', 'LemonStand'), ('Lilypond', 'Lilypond'), ('Lithium', 'Lithium'), ('Magento', 'Magento'), ('Maven', 'Maven'), ('Mercury', 'Mercury'), ('MetaProgrammingSystem', 'MetaProgrammingSystem'), ('Meteor', 'Meteor'), ('Node', 'Node'), ('OCaml', 'OCaml'), ('Objective-C', 'Objective-C'), ('Opa', 'Opa'), ('OracleForms', 'OracleForms'), ('Packer', 'Packer'), ('Perl', 'Perl'), ('Phalcon', 'Phalcon'), ('PlayFramework', 'PlayFramework'), ('Plone', 'Plone'), ('Prestashop', 'Prestashop'), ('Processing', 'Processing'), ('Python', 'Python'), ('Qooxdoo', 'Qooxdoo'), ('Qt', 'Qt'), ('R', 'R'), ('ROS', 'ROS'), ('Rails', 'Rails'), ('RhodesRhomobile', 'RhodesRhomobile'), ('Ruby', 'Ruby'), ('Rust', 'Rust'), ('SCons', 'SCons'), ('Sass', 'Sass'), ('Scala', 'Scala'), ('Scrivener', 'Scrivener'), ('Sdcc', 'Sdcc'), ('SeamGen', 'SeamGen'), ('SketchUp', 'SketchUp'), ('SugarCRM', 'SugarCRM'), ('Swift', 'Swift'), ('Symfony', 'Symfony'), ('SymphonyCMS', 'SymphonyCMS'), ('Target3001', 'Target3001'), ('Tasm', 'Tasm'), ('TeX', 'TeX'), ('Textpattern', 'Textpattern'), ('TurboGears2', 'TurboGears2'), ('Typo3', 'Typo3'), ('Umbraco', 'Umbraco'), ('Unity', 'Unity'), ('VVVV', 'VVVV'), ('VisualStudio', 'VisualStudio'), ('Waf', 'Waf'), ('WordPress', 'WordPress'), ('Xojo', 'Xojo'), ('Yeoman', 'Yeoman'), ('Yii', 'Yii'), ('ZendFramework', 'ZendFramework'), ('Zephir', 'Zephir'), ('gcov', 'gcov'), ('nanoc', 'nanoc'), ('opencart', 'opencart'), ('stella', 'stella')], db_index=True, max_length=30),
            preserve_default=True,
        ),
    ]
