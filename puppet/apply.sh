#!/bin/bash
sudo puppet apply --modulepath openjdk-dev/modules/ openjdk-dev/manifests/sites.pp
