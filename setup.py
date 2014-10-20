#!/usr/bin/env python

from setuptools import setup, find_packages

RPM_REQUIRED_DEPS = "python-argparse PyYAML python-dateutil python-json"
 
## HACK FOR DEPS IN RPMS
from setuptools.command.bdist_rpm import bdist_rpm
def custom_make_spec_file(self):
    spec = self._original_make_spec_file()
    lineDescription = "%description"
    spec.insert(spec.index(lineDescription) - 1, "requires: %s" % RPM_REQUIRED_DEPS)
    return spec
bdist_rpm._original_make_spec_file = bdist_rpm._make_spec_file
bdist_rpm._make_spec_file = custom_make_spec_file
## END OF HACK

setup(
    name = "mmbackupagent",
    version = "0.1",
    packages = find_packages(),
    entry_points = {
        'console_scripts': ['mmbackupagent=mmbackupagent.cmdline:main'],
    }
)
