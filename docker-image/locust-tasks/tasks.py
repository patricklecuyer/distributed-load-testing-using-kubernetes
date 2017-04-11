#!/usr/bin/env python

# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import uuid
import random

from locust import HttpLocust, TaskSet, task


class MetricsTaskSet(TaskSet):
    _deviceid = None
    _wordlist = []

    def on_start(self):
        self._deviceid = str(uuid.uuid4())
        with open('/vocab.txt') as f:
            self._wordlist = f.readlines()
        

    @task(999)
    def suggest(self):
        w = self._wordlist[random.randint(0, len(self._wordlist))]
        q = w[:random.randint(2, len(w))]

        self.client.get(
            '/complete?q=%q' % q)

    @task(999)
    def search(self):
        q = self._wordlist[random.randint(0, len(self._wordlist))]
        self.client.get(
            '/suggest?q=%q' % q)


class MetricsLocust(HttpLocust):
    task_set = MetricsTaskSet
