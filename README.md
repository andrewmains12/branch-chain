# branch-chain: utilities for dealing with chains of git branches

branch-chain is a small command line utility for keeping your git branches together.

## Quickstart

TODO: put this in pypi

### Bootstrap
```
   # you may need to run as root
   git clone https://github.com/andrewmains12/branch-chain.git
   cd branch-chain
   python setup.py install
```

### Running 

```
rebase-chain --help
usage: rebase-chain [-h] [-s START] [-ni] [--force-push]
                    [--diff-message DIFF_MESSAGE]
                    {push,rebase,arc,all} to_rebase

Rebase a chain of branches

positional arguments:
  {push,rebase,arc,all}
                        The thing to do
  to_rebase             File containing new line delimited list of branches to
                        rebase

optional arguments:
  -h, --help            show this help message and exit
  -s START, --start START
  -ni, --no-interactive
                        Run rebases without -i
  --force-push          git force push (push -f)
  --diff-message DIFF_MESSAGE
                        Message to use with arc diff
```

TODO: runnable example.

## Motivation 
This utility comes out of my experience developing with a team. Whenever I write medium to large features, there's an inherent tension between the desire to make all of 
my changes at once (if the code's flowing, it never seems like a good idea to stop) and the need to break my commits down into digestible chunks for the team. It's much 
easier to *write* a 5000 line diff than it is to review one.

"Stacked" diffs--changes branched off of one another in digestible chunks--are a good solution to this problem, but they cause another one--you now have to keep your branches together. rebase-chain solves that problem for you.
