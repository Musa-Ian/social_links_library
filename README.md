# Social Links Library

## Looking for Maintainers & Contributors

I created this project to help the community, but I am not a developer and am looking for others to help maintain and improve it!
If you want to be a collaborator or maintainer, please reach out to me on Reddit: [u/Far-Professional4417](https://www.reddit.com/user/Far-Professional4417/).

Feel free to open issues, submit pull requests, or suggest improvements!

A universal, open-source tool to keep track of real-time social media profile link structures for all major platforms. This project aims to provide developers and apps with always-up-to-date, reliable patterns for constructing and validating social media profile URLs.

## Why?
Social media platforms frequently change their URL structures, breaking integrations and apps. This library is a community-driven, API-first solution to keep everyone in sync.

## How it Works
- **Central JSON file** (`data/social_links.json`) contains up-to-date link patterns for each platform.
- **API and SDKs** (coming soon) will provide easy access for all programming languages.
- **Community contributions** keep the data fresh and accurate.

## Data Structure
Each entry in `data/social_links.json` looks like this:
```json
{
  "platform": "x",
  "display_name": "X (formerly Twitter)",
  "url_pattern": "https://x.com/{username}",
  "validation_regex": "^[A-Za-z0-9_]{1,15}$",
  "example": "https://x.com/elonmusk",
  "last_verified": "2025-06-20"
}
```

## Roadmap
- [x] Define initial schema and data (2025)
- [x] Build REST API to serve data (2025)
- [ ] Create SDKs for JS, Python, and more (2025)
- [ ] Add automated monitoring for link changes (2025)
- [ ] Grow community and contributions (2025)

## Contributing
1. Fork the repo and create a branch.
2. Edit `data/social_links.json` to add or update a platform.
3. Open a Pull Request with your changes.
4. See `docs/CONTRIBUTING.md` for more details (coming soon).

## License
MIT 