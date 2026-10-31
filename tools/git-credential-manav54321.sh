#!/bin/sh
# Git credential helper for the House-of-diams repos in storefront/ and admin/.
# Supplies the Manav54321 token from the workspace .env; holds no secret itself.
[ "$1" = get ] || exit 0
ENV_FILE="/Users/manavdesai/Desktop/HOD SEO/.env"
token=$(grep '^GITHUB_TOKEN_MANAV54321=' "$ENV_FILE" | tail -1 | cut -d= -f2-)
[ -n "$token" ] || exit 0
echo username=Manav54321
echo "password=$token"
