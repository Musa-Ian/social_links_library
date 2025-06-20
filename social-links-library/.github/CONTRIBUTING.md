# Contributing to Social Links Library

Thank you for your interest in contributing!

## How to Contribute
1. Fork the repository and create a new branch.
2. Edit `data/social_links.json` to add or update a social media platform's link pattern.
3. Make sure your entry includes:
   - `platform` (unique key)
   - `display_name`
   - `url_pattern` (with `{username}` placeholder)
   - `validation_regex` (for usernames)
   - `example` (valid example link)
   - `last_verified` (date you checked the pattern)
4. Open a Pull Request with a clear description of your changes.
5. Your PR will be reviewed and merged if it meets the guidelines.

## Guidelines
- Double-check the accuracy of the link pattern and regex.
- Use the current date for `last_verified` if you checked the pattern.
- Be respectful and constructive in discussions.

Thank you for helping keep this library up to date! 