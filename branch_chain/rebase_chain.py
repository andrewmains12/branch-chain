#!/usr/bin/env python

# Rebase a chain of branches
import argparse
import subprocess
import sys


def get_current_branch():
    return subprocess.check_output("git symbolic-ref HEAD", shell=True).strip().split("/")[-1]


def rebase_onto(onto, cur_branch, interactive=True):
    cmd = ("git rebase %(interactive)s --fork-point --onto %(onto)s %(onto)s %(cur_branch)s" % {
        "interactive": "-i" if interactive else "",
        "onto": onto,
        "cur_branch": cur_branch})
    print cmd
    subprocess.check_call(
        cmd,
        shell=True)


def push(branch, force_push=False):
    # hack to prevent accidents
    if branch == "master":
        raise ValueError("Not pushing master for you")

    force_opt = "-f" if force_push else ""
    subprocess.check_call(
        "git push %s origin %s" % (force_opt, branch),
        shell=True
    )


def wait_until_confirmation(msg):
    should_continue = False
    while not should_continue:
        should_continue = raw_input("%s (y/n)" % msg).strip() == 'y'


def rebase_chain(branches, starting_branch, no_interactive=False):
    starting_idx = branches.index(starting_branch) - 1

    if starting_idx < 0:
        raise ValueError("Starting branch needs one predecessor")

    branches = branches[starting_idx:]

    for i, branch in enumerate(branches[1:], 1):
        prev_branch = branches[i - 1]
        try:
            rebase_onto(prev_branch, branch, interactive=not no_interactive)
        except subprocess.CalledProcessError:
            wait_until_confirmation("Conflict's fixed?")


def arc_diff_onto(prev_branch, branch, message):
    subprocess.check_call("git checkout %s" % branch, shell=True)

    subprocess.check_call(["arc", "diff", prev_branch, "--message", message, "--allow-untracked"])


def arc_diff_chain(branches, starting_branch, message='rebase'):
    starting_idx = branches.index(starting_branch) - 1

    if starting_idx < 0:
        raise ValueError("Starting branch needs one predecessor")

    branches = branches[starting_idx:]

    for i, branch in enumerate(branches[1:], 1):
        prev_branch = branches[i - 1]
        arc_diff_onto(prev_branch, branch, message=message)


def push_chain(branches, starting_branch, force_push=False):
    starting_idx = branches.index(starting_branch)

    for branch in branches[starting_idx:]:
        push(branch, force_push=force_push)


#########################################
# Actions
#########################################

def rebase_action(branches, starting_branch, opts):
    return rebase_chain(branches, starting_branch, no_interactive=opts.no_interactive)


def push_action(branches, starting_branch, opts):
    return push_chain(branches, starting_branch, force_push=opts.force_push)


def arc_action(branches, starting_branch, opts):
    return arc_diff_chain(branches, starting_branch, opts.diff_message)


def all_action(branches, starting_branch, opts):
    rebase_action(branches, starting_branch, opts)
    push_action(branches, starting_branch, opts)
    arc_action(branches, starting_branch, opts)


ACTIONS = {
    'rebase': rebase_action,
    'push': push_action,
    'arc': arc_action,
    'all': all_action
}


def parse_starting_branch(branches, start):
    if start == "CURRENT":
        return get_current_branch()
    elif start == "START":
        return branches[1]

    return start


def main():
    parser = argparse.ArgumentParser(description="Rebase a chain of branches")

    parser.add_argument("action", help="The thing to do", choices=ACTIONS.keys())
    parser.add_argument("to_rebase",
                        help="File containing new line delimited list of branches to rebase")

    parser.add_argument("-s", "--start", default="CURRENT",
                        help="""The name of the branch to start on. We respect 2 special values here:
    CURRENT: the current branch (default)
    START: the *second* branch in the list (the first should be master/the based)
"""
    )
    parser.add_argument('-ni', "--no-interactive", help="Run rebases without -i", action='store_true')
    parser.add_argument('--force-push', help='git force push (push -f)', action='store_true')
    parser.add_argument('--diff-message', help='Message to use with arc diff', default='rebase')

    args = parser.parse_args()

    with open(args.to_rebase) as f:
        branches = [line.strip() for line in f]

    starting_branch = parse_starting_branch(branches, args.start)

    print "Starting on %s" % starting_branch

    print "Performing %s on %s" % (args.action, branches)
    ACTIONS[args.action](branches, starting_branch, args)


if __name__ == "__main__":
    main()
