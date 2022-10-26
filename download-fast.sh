#!/bin/bash
grep DL | sed 's/DL: \[//' | sed 's/\] -> \[/\n dir=/' | sed 's/\]//' | aria2c -i - -Z false -j 20