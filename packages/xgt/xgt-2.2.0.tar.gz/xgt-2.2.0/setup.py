# -*- coding: utf-8 -*- ----------------------------------------------------===#
#
#  Copyright 2016-2025 Trovares Inc. dba Rocketgraph.  All rights reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#===------------------------------------------------------------------------===#

import os.path
from setuptools import setup, find_packages

basedir = os.path.dirname(__file__)
with open(os.path.join(basedir,'requirements.txt')) as f:
  requirements = f.read().splitlines()

setup(packages=find_packages('src'),
      package_dir={'':'src'},
      include_package_data=True,
      install_requires=requirements,
      extras_require={
        'extra': ['pandas>=0.24.2', 'jupyter'],
      }
)
