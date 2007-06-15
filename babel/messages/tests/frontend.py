# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Edgewall Software
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://babel.edgewall.org/wiki/License.
#
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at http://babel.edgewall.org/log/.

from distutils.dist import Distribution
from distutils.errors import DistutilsOptionError, DistutilsSetupError
from distutils.log import _global_log
import doctest
import os
import time
import unittest

from babel import __version__ as VERSION
from babel.messages import frontend


class ExtractMessagesTestCase(unittest.TestCase):

    def setUp(self):
        self.olddir = os.getcwd()
        self.datadir = os.path.join(os.path.dirname(__file__), 'data')
        os.chdir(self.datadir)
        _global_log.threshold = 5 # shut up distutils logging

        self.dist = Distribution(dict(
            name='TestProject',
            version='0.1',
            packages=['project']
        ))
        self.cmd = frontend.extract_messages(self.dist)
        self.cmd.initialize_options()

    def tearDown(self):
        pot_file = os.path.join(self.datadir, 'project', 'i18n', 'messages.pot')
        if os.path.isfile(pot_file):
            os.unlink(pot_file)

        os.chdir(self.olddir)

    def test_neither_default_nor_custom_keywords(self):
        self.cmd.output_file = 'foobar'
        self.cmd.no_default_keywords = True
        self.assertRaises(DistutilsOptionError, self.cmd.finalize_options)

    def test_no_output_file_specified(self):
        self.assertRaises(DistutilsOptionError, self.cmd.finalize_options)

    def test_both_sort_output_and_sort_by_file(self):
        self.cmd.output_file = 'foobar'
        self.cmd.sort_output = True
        self.cmd.sort_by_file = True
        self.assertRaises(DistutilsOptionError, self.cmd.finalize_options)

    def test_extraction_with_default_mapping(self):
        self.cmd.copyright_holder = 'FooBar, Inc.'
        self.cmd.msgid_bugs_address = 'bugs.address@email.tld'
        self.cmd.output_file = 'project/i18n/messages.pot'
        self.cmd.add_comments = 'TRANSLATOR:,TRANSLATORS:'

        self.cmd.finalize_options()
        self.cmd.run()
        self.assertEqual(open(os.path.join(self.datadir, 'project', 'i18n',
                                           'messages.pot'), 'U').read(),
r"""# Translations template for TestProject.
# Copyright (C) %(year)s FooBar, Inc.
# This file is distributed under the same license as the TestProject
# project.
# FIRST AUTHOR <EMAIL@ADDRESS>, %(year)s.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: TestProject 0.1\n"
"Report-Msgid-Bugs-To: bugs.address@email.tld\n"
"POT-Creation-Date: %(date)s\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=utf-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: Babel %(version)s\n"

#. This will be a translator coment,
#. that will include several lines
#: project/file1.py:8
msgid "bar"
msgstr ""

#: project/file2.py:9
msgid "foobar"
msgid_plural "foobars"
msgstr[0] ""
msgstr[1] ""

#: project/CVS/this_wont_normally_be_here.py:11
msgid "FooBar"
msgid_plural "FooBars"
msgstr[0] ""
msgstr[1] ""

""" % {'version': VERSION,
       'year': time.strftime('%Y'),
       'date': time.strftime('%Y-%m-%d %H:%M%z')})

    def test_extraction_with_mapping_file(self):
        self.cmd.copyright_holder = 'FooBar, Inc.'
        self.cmd.msgid_bugs_address = 'bugs.address@email.tld'
        self.cmd.mapping_file = 'mapping.cfg'
        self.cmd.output_file = 'project/i18n/messages.pot'
        self.cmd.add_comments = 'TRANSLATOR:,TRANSLATORS:'

        self.cmd.finalize_options()
        self.cmd.run()
        self.assertEqual(open(os.path.join(self.datadir, 'project', 'i18n',
                                           'messages.pot'), 'r').read(),
r"""# Translations template for TestProject.
# Copyright (C) %(year)s FooBar, Inc.
# This file is distributed under the same license as the TestProject
# project.
# FIRST AUTHOR <EMAIL@ADDRESS>, %(year)s.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: TestProject 0.1\n"
"Report-Msgid-Bugs-To: bugs.address@email.tld\n"
"POT-Creation-Date: %(date)s\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=utf-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: Babel %(version)s\n"

#. This will be a translator coment,
#. that will include several lines
#: project/file1.py:8
msgid "bar"
msgstr ""

#: project/file2.py:9
msgid "foobar"
msgid_plural "foobars"
msgstr[0] ""
msgstr[1] ""

""" % {'version': VERSION,
       'year': time.strftime('%Y'),
       'date': time.strftime('%Y-%m-%d %H:%M%z')})

    def test_extraction_with_mapping_dict(self):
        self.dist.message_extractors = {
            'project': [
                ('**/CVS/**.*', 'ignore',   None),
                ('**.py',       'python',   None),
            ]
        }
        self.cmd.copyright_holder = 'FooBar, Inc.'
        self.cmd.msgid_bugs_address = 'bugs.address@email.tld'
        self.cmd.output_file = 'project/i18n/messages.pot'
        self.cmd.add_comments = 'TRANSLATOR:,TRANSLATORS:'

        self.cmd.finalize_options()
        self.cmd.run()
        self.assertEqual(open(os.path.join(self.datadir, 'project', 'i18n',
                                           'messages.pot'), 'r').read(),
r"""# Translations template for TestProject.
# Copyright (C) %(year)s FooBar, Inc.
# This file is distributed under the same license as the TestProject
# project.
# FIRST AUTHOR <EMAIL@ADDRESS>, %(year)s.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: TestProject 0.1\n"
"Report-Msgid-Bugs-To: bugs.address@email.tld\n"
"POT-Creation-Date: %(date)s\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=utf-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: Babel %(version)s\n"

#. This will be a translator coment,
#. that will include several lines
#: project/file1.py:8
msgid "bar"
msgstr ""

#: project/file2.py:9
msgid "foobar"
msgid_plural "foobars"
msgstr[0] ""
msgstr[1] ""

""" % {'version': VERSION,
       'year': time.strftime('%Y'),
       'date': time.strftime('%Y-%m-%d %H:%M%z')})


def suite():
    suite = unittest.TestSuite()
    suite.addTest(doctest.DocTestSuite(frontend))
    suite.addTest(unittest.makeSuite(ExtractMessagesTestCase))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')