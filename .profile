# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
	. "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin directories
PATH="$HOME/bin:$HOME/.local/bin:$PATH"
#----------CUSTOM STUFF STARTS HERE (this line included)----------
export BROWSER='/mnt/c/Program Files/Mozilla Firefox/firefox.exe'
SCRIPTS=/mnt/c/Users/Muhznit/gitrepos

if test "${PS1+set}"; then
    CDPATH=.:~:..:$SCRIPTS
fi


# Jump to directory by name alone. This should be on by default
shopt -s autocd

#GIT_PS1_SHOWDIRTYSTATE=true
#export PS1='\u@\w$(__git_ps1)\$ '

# No cd ../../.., no cd ......, just type "up" and the directory name.
_up() {
    local cur=${COMP_WORDS[COMP_CWORD]}
    words=$(echo $PWD | sed -e "s/\/home\/$USER\/\(.*\)\/[^/].*$/\1/" -e "s/ /\\\ /g")
    #words=$(echo $PWD | sed -e "s/\(.*\)\/[^/].*$/\1/" -e "s/ /\\\ /g")
    words=(${words////$'\n'})
    words=${words[@]}
    COMPREPLY=( $(compgen -W "$words" -- $cur) )
}

up() {
    cd $(echo $PWD | sed -e "s/$1.*/$1/")
}

complete -F _up up

# Edit stuff in $SCRIPTS from anywhere
_vich() {
    local cur=${COMP_WORDS[COMP_CWORD]}
    words=$(find $SCRIPTS -regex ".*$cur.*.py" | xargs -I % basename %)
    COMPREPLY=( $(compgen -W "$words" -- $cur) )
}

vich() {
    vi $SCRIPTS/$@
}

complete -F _vich vich

# Jump to the $PWD of other terminals.
_wd() {
    local cur=${COMP_WORDS[COMP_CWORD]}
    local exp="s/^n\(..*\)/\"\1\"/p"
    words=$(pgrep 'bash' | xargs -I % lsof -a -d cwd -F -p % | sed -n -e $exp | sort -u)
    IFS=$'\n'
    COMPREPLY=( $(compgen -W "$words" -- $cur | sed -e 's/\(.*\)/\"\1\"/') )
    IFS=$' \t\n'
}

wd() {
    cd "$1"
}

complete -F _wd wd
