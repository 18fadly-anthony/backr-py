#!/bin/bash

if [ ! -f ~/.local/bin/backr.py ]; then
  ln -s $(pwd)"/backr.py" ~/.local/bin/
fi

if [ ! -f ~/.local/bin/restor.py ]; then
  ln -s $(pwd)"/restor.py" ~/.local/bin/
fi

if [ ! -d ~/backrs ]; then
  mkdir ~/backrs
fi
