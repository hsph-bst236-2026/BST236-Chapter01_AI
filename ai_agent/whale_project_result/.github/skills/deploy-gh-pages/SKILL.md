---
name: deploy-gh-pages
description: Deploys the generated HTML dashboard to GitHub Pages by committing to the gh-pages branch. Use this skill when you need to publish or update the live dashboard.
---

# Deploy to GitHub Pages

## Instructions

1. Ensure the generated report exists at `docs/index.html`.

2. Configure git user for the commit:
   ```bash
   git config user.name "Crypto Watchtower Bot"
   git config user.email "watchtower-bot@users.noreply.github.com"
   ```

3. Check if the `gh-pages` branch exists:
   ```bash
   git ls-remote --heads origin gh-pages
   ```

4. **If `gh-pages` does NOT exist**, create it as an orphan branch:
   ```bash
   git checkout --orphan gh-pages
   git rm -rf .
   cp docs/index.html index.html
   git add index.html
   git commit -m "🐋 Initial dashboard deployment"
   git push origin gh-pages
   git checkout main
   ```

5. **If `gh-pages` EXISTS**, update it:
   ```bash
   git stash --include-untracked
   git checkout gh-pages
   cp docs/index.html index.html
   git add index.html
   git commit -m "🐋 Dashboard update — $(date -u '+%Y-%m-%d %H:%M UTC')"
   git push origin gh-pages
   git checkout main
   git stash pop || true
   ```

6. Print the GitHub Pages URL:
   ```
   Dashboard deployed to: https://<owner>.github.io/<repo>/
   ```

## Error Handling

- If `docs/index.html` does not exist, abort and print: "❌ No report found at docs/index.html — run the report generator first."
- If git push fails, print the error and suggest checking repository permissions.
- Always return to the `main` branch after deployment, even if errors occur.
