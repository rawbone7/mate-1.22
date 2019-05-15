#!/bin/bash

spectool -g -C sources/ $1
rpmbuild -bs $1

