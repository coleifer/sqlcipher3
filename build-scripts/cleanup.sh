#!/bin/bash

cleanup="openssl-OpenSSL_1_1_1b sqlcipher sqlcipher3 wheelhouse"
for p in $cleanup; do
  if [[ -d "$p" ]]; then
    sudo rm -rf "$p"
  fi
done
