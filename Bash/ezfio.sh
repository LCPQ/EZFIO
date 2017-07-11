#!/bin/bash

EZFIO_ROOT=$( cd $(dirname "${BASH_SOURCE}")/..  ; pwd -P )

function _ezfio_py()
{
  python ${EZFIO_ROOT}/Python/ezfio.py $@
}


function _ezfio_usage()
{
      echo "
Usage:
  ezfio set_file    EZFIO_DIRECTORY
  ezfio unset_file 

  ezfio has         DIRECTORY   ITEM
  ezfio get         DIRECTORY   ITEM
  ezfio set         DIRECTORY   ITEM  VALUE  : Scalar values
  ezfio set         DIRECTORY   ITEM         : Array values read from stdin

  ezfio set_verbose
  ezfio unset_verbose
"
}

function _require_ezfio_file()
{
  if [[ -z ${EZFIO_FILE} ]]
  then
    echo "EZFIO directory not set: try 'ezfio set_file'"
    return 1
  fi

  if [[ ! -d ${EZFIO_FILE} ]]
  then
    echo "EZFIO directory not accessible: try 'ezfio set_file'"
    return 1
  fi
}

function _require_first_argument()
{
  if [[ -z $1 ]]
  then
    _ezfio_usage
    echo "Error: First argument not set"
    return 1
  else
    return 0
  fi
}

function _require_second_argument()
{
  if [[ -z $2 ]]
  then
    _ezfio_usage
    echo "Error: Second argument not set"
    return 1
  fi
}

function _ezfio_set_verbose()
{
  function _ezfio_info()
  {
    echo "$1"
  }
  return 0
}

function _ezfio_unset_verbose()
{
  function _ezfio_info()
  {
    :
  }
  return 0
}

function _ezfio_set_file()
{
  _require_first_argument $@ || return 1

  if [[ ! -d $1 ]]
  then
    mkdir -p $1 || return 1
  fi
  export EZFIO_FILE=$1
  _ezfio_info "Set file ${EZFIO_FILE}"
  return 0
}

function _ezfio_unset_file()
{
  _require_ezfio_file || return 1
  _ezfio_info "Unset file ${EZFIO_FILE}"
  unset EZFIO_FILE
  return 0
}

function _ezfio_has()
{
  _require_ezfio_file        || return 1
  _require_first_argument $@ || return 1
  
  if [[ ! -d ${EZFIO_FILE}/${1,,} ]]
  then
      return 1
  fi
  
  if [[ -z $2 ]]
  then
      return 0
  fi

  _ezfio_py has $@ && return 0 || return 1
}

function _ezfio_get()
{
  _require_ezfio_file        || return 1

  if [[ -z $1 ]] 
  then
    ls ${EZFIO_FILE} && return 0 || return 1
  fi

  if [[ -z $2 ]]
  then
      ls ${EZFIO_FILE}/${1,,} && return 0 || return 1
  fi

  _ezfio_py get $@ && return 0 || return 1
}

function _ezfio_set()
{
  _require_ezfio_file         || return 1
  _require_first_argument  $@ || return 1
  _require_second_argument $@ || return 2

  if [[ -z $3 ]]
  then
    _ezfio_py set $@ || return 1
  else
    echo $3 | _ezfio_py set $1 $2 || return 1
  fi
  return 0
}

#---

function ezfio()
{
  case $1 in 
    "has")
      shift
      _ezfio_has $@
      ;;

    "set")
      shift
      _ezfio_set $@
      ;;

    "get")
      shift
      _ezfio_get $@
      ;;

    "set_file")
      shift
      _ezfio_set_file $@
      ;;

    "unset_file")
      shift
      _ezfio_unset_file 
      ;;

    "set_verbose")
      _ezfio_set_verbose
      ;;

    "unset_verbose")
      _ezfio_unset_verbose
      ;;

    *)
      _ezfio_usage
      ;;
  esac

}


_ezfio_unset_verbose


# Completion


_Complete()
{
  local cur

  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"
  prev2="${COMP_WORDS[COMP_CWORD-2]}"

  if [[ -n ${EZFIO_FILE} && -d ${EZFIO_FILE} ]]
  then

    case "${prev2}" in
      set|has|get)
        COMPREPLY=( $(compgen -W "$(cd ${EZFIO_FILE}/${prev} ; ls | sed 's/\.gz//' )" -- $cur ) )
        return 0
        ;;
    esac

    case "${prev}" in
      unset_file|set_verbose|unset_verbose)
        COMPREPLY=()
        return 0
        ;;
      set|has|get)
        COMPREPLY=( $(compgen -W "$(cd ${EZFIO_FILE} ; \ls -d */ | sed 's|/||g')" -- $cur ) )
        return 0
        ;;
      *)
        COMPREPLY=( $(compgen -W 'has get set unset_file \
                                  set_verbose unset_verbose -h' -- $cur ) )
        return 0
        ;;
    esac

  else

    case "${prev}" in
      set_verbose|unset_verbose)
        COMPREPLY=()
        return 0
        ;;
      set_file)
        COMPREPLY=( $(compgen -W "$(\ls -d */ | sed 's|/||g')" -- ${cur} ) )
        return 0
        ;;
      *)
        COMPREPLY=( $(compgen -W 'set_file \
                                  set_verbose unset_verbose -h' -- $cur ) )
        return 0
        ;;
    esac

  fi
}

complete -F _Complete ezfio
