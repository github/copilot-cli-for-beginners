# Security Notes

## Scope

This note covers secret hygiene for the course repository, with emphasis on preventing accidental commits of local credentials and certificate material.

## What Was Checked

- Root `.gitignore` coverage for common environment files
- Root `.gitignore` coverage for private keys and certificate bundles
- Repository search for obvious secret-like strings and hard-coded credentials

## Hygiene Improvements Made

- Added ignore rules for common secret and certificate artifacts:
  - `*.pem`
  - `*.key`
  - `*.crt`
  - `*.cer`
  - `*.pfx`
  - `*.p12`
  - `secrets.*`

## Findings

- `.env` and `.env.*.local` patterns were already ignored.
- The repository contains intentionally insecure examples under `samples/buggy-code/` for teaching purposes. Those files were not changed because the course instructions explicitly keep those bugs in place.
- The broader repository should avoid committing local key, certificate, or bundled secret files, which is why the ignore rules were expanded.

## Recommended Practice

- Keep real credentials out of the repo and load them from local environment configuration.
- Treat generated certificates, private keys, and exported credential bundles as untracked local artifacts.
- Review staged files before each commit with `git diff --staged`.