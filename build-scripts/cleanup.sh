#!/bin/bash

cleanup="openssl-openssl-3.5.4 sqlcipher sqlcipher3 wheelhouse"
for p in $cleanup; do
  if [[ -d "$p" ]]; then
    sudo rm -rf "$p"
  fi
done
