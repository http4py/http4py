default:
    @just --list

check:
    ./scripts/http4py.sh check

# see https://github.com/casey/just

_recipes:
    @just --list --unsorted --list-heading $'Available recipes:\n' --list-prefix "  "

# serves the static site
@serve:
    #!/usr/bin/env sh
    interfaces=$(ifconfig -l | tr ' ' '\n' | grep '^en')
    base_url=$(
      if test "$(uname -s)" == "Darwin"
      then
        for interface in $interfaces; do
            ip_address=$(ipconfig getifaddr $interface 2>/dev/null)

            if [ -n "$ip_address" ]; then
                echo "$ip_address"
                exit 0
            fi
        done
      else
        hostname --ip-address
      fi
    )
    hugo server \
      --baseURL=http://${base_url} \
      --bind=0.0.0.0 \
      --source=website \
      --buildDrafts \
      --disableFastRender \
      --navigateToChanged

# installs dependencies
@install:
    brew install hugo
    git submodule update --init --recursive
