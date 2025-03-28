################################
Heimdall - Heurist XML connector
################################

.. image:: https://img.shields.io/badge/license-AGPL3.0-informational?logo=gnu&color=success
   :target: https://www.gnu.org/licenses/agpl-3.0.html
.. image:: https://www.repostatus.org/badges/latest/unsupported.svg
   :target: https://www.repostatus.org/#project-statuses
.. image:: https://img.shields.io/badge/documentation-api-green
   :target: https://datasphere.readthedocs.io/projects/heimdall/
.. image:: https://gitlab.huma-num.fr/datasphere/heimdall/connectors/heurist/badges/main/pipeline.svg
   :target: https://gitlab.huma-num.fr/datasphere/heimdall/connectors/heurist/pipelines/latest
.. image:: https://gitlab.huma-num.fr/datasphere/heimdall/connectors/heurist/badges/main/coverage.svg
   :target: https://datasphere.gitpages.huma-num.fr/heimdall/connectors/heurist/coverage/index.html

*************
What is this?
*************

`Heimdall <https://datasphere.readthedocs.io/projects/heimdall/>`_ is a tool for converting more easily one or more databases from one format to another.
It leverages modules called "connectors", responsible for conversion of data between specific databases schemas and the HERA format.

This repository contains a connector to Heurist's own XML export format (HML).

********************
Why should I use it?
********************

You can use this connector, along with the `pyheimdall software <https://gitlab.huma-num.fr/datasphere/heimdall/python>`_, to retrieve any data exported from Heurist.
You can then aggregate this data into your research corpus easily, for example using other Heimdall connectors.

| Take note, however that some legal restrictions might apply to data retrieved from any scientific database.
| Plus, if at the end of your project, you share your data, please cite the original data properly.

*****************
How can I use it?
*****************

Setup
=====

This pyHeimdall connector is available as a `PyPI package <https://pypi.org/project/pyheimdall-heurist/>`_ named ``pyheimdall-heurist``.
You can install it using the `pip <https://pip.pypa.io/en/stable/>`_ package manager:

.. code-block:: bash

   pip install pyheimdall-heurist

You can use `pip <https://pip.pypa.io/en/stable/>`_ to either upgrade or uninstall this connector, too:

.. code-block:: bash

   pip install --upgrade pyheimdall-heurist
   pip uninstall pyheimdall-heurist



Usage
=====

.. code-block:: python

   import heimdall

   tree = heimdall.getDatabase(format='heurist:xml', url='Export_db_AAAAMMDDHHMMSS.xml')
   heimdall.createDatabase(tree, format='csv', url='.')

Please note that you shouldn't use ``pyheimdall-heurist`` functions directly.
As long as the package is installed on your system, pyHeimdall will automatically discover its features and allow you to use them as long as any other `default <https://gitlab.huma-num.fr/datasphere/heimdall/python/-/tree/main/src/heimdall/connectors>`_ or `external <https://gitlab.huma-num.fr/datasphere/heimdall/connectors>`_ connector.

*************
Is it tested?
*************

Well, yes … and no.

| As you can see in our badge list, or in this `coverage report <https://datasphere.gitpages.huma-num.fr/heimdall/connectors/heurist/coverage/index.html>`_, the code coverage by our unit tests is not too shabby.
  However, to validate their behaviour, these tests take the file ``/tests/resources/heurist.xml`` as an input, which simulates an exported XML ("HML") file from Heurist.
|  And this is where the problem lies.
| At the time of writing (early 2025), Heurist still has an outdated comunity management and is full of undocumented behaviours.
  Among these, the "HML" file remains unspecified, the link to its XSD is broken, and Heurist doesn't even behave as expected, when one feeds it its own output.
  So, this connector really tries its best to deduce how stuff seems to work in most cases.
| This as two limits, though.

* First, those assumptions can be wrong, or incomplete.
  Still at the time of writing, the Heurist core development team seems unable to document its own output, so … well.
* Second, even if everybody seems fine today, the Heurist core development team is known to force unto its userbase new (sometimes breaking) updates without any prior notice, documentation or regression testing.
  Of course, this means that the ``/test/resources/heurist.xml`` file may become outdated with time, and this connector won't automagically warn you of any problem.

| Unit testing with a static test file is, of course, not ideal.
  But (you know the drill: "at time of writing") Heurist is devoid of any machine-usable API, let alone RESTful.
  So there isn't really any other choice.
| As you may understand, by design of its own creator, third party softwares trying to be interoperable with Heurist are just … well, f•••ed.

| To conclude: depending on when you read this, you can install this connector, try to load a recently exported XML (HML) file, and if it doesn't work, you're probably f•••ed, too.
| That is, unless you contribute, of course.

*********************
How can I contribute?
*********************

PyHeimdall welcomes any feedback or proposal.
Details can be accessed `here <https://gitlab.huma-num.fr/datasphere/heimdall/python/-/blob/main/CONTRIBUTING.rst>`_

*******
License
*******

`GNU Affero General Public License version 3.0 or later <https://choosealicense.com/licenses/agpl/>`_
