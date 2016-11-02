#!/bin/bash
sudo puppet apply --noop --modulepath openjdk-dev/modules/ openjdk-dev/manifests/sites.pp
