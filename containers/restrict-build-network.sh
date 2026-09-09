#!/bin/bash
# Host enforcement for the explicitly online public-dependency preparation phase.
set -euo pipefail
uid=$(id -u corpus)
iptables -N CORPUS_EGRESS 2>/dev/null || true
iptables -F CORPUS_EGRESS
iptables -C OUTPUT -m owner --uid-owner "$uid" -j CORPUS_EGRESS 2>/dev/null || \
  iptables -I OUTPUT 1 -m owner --uid-owner "$uid" -j CORPUS_EGRESS
# Permit DNS only on the host's stub and Google's resolver, not HTTP metadata.
for resolver in 127.0.0.53/32 169.254.169.254/32; do
  iptables -A CORPUS_EGRESS -d "$resolver" -p udp --dport 53 -j ACCEPT
  iptables -A CORPUS_EGRESS -d "$resolver" -p tcp --dport 53 -j ACCEPT
done
for cidr in 169.254.0.0/16 10.0.0.0/8 172.16.0.0/12 192.168.0.0/16 127.0.0.0/8; do
  iptables -A CORPUS_EGRESS -d "$cidr" -j REJECT
done
iptables -A CORPUS_EGRESS -p tcp -m multiport --dports 80,443 -j ACCEPT
iptables -A CORPUS_EGRESS -p udp --dport 53 -j ACCEPT
iptables -A CORPUS_EGRESS -j REJECT
# No IPv6 bypass. This build host and its container network use IPv4.
ip6tables -C OUTPUT -m owner --uid-owner "$uid" -j REJECT 2>/dev/null || \
  ip6tables -I OUTPUT 1 -m owner --uid-owner "$uid" -j REJECT
