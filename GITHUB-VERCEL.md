# Online deployment — GitHub Pages & Vercel

This project is a complete static site. **Upload the SOURCE project** (including `package.json`, `src/`, `public/`, `.github/`) to GitHub, not the built `dist/` folder alone. The workflow publishes the game automatically. GitHub Pages and Vercel are two alternative hosting methods: choose either one.

## A. GitHub upload in your browser (simplest)

1. Sign in at https://github.com/new.
2. Create a new repository named `math-adventure-fraction-kingdom` under your GitHub account. Choose **Public** for free public GitHub Pages hosting. Leave the GitHub initialize README option unchecked (our project already has one).
3. Extract the project ZIP and open the `math-adventure-online-github` folder.
4. In the new repository, click **uploading an existing file** / **Add file → Upload files**. Drag the **contents of the extracted folder**, not the folder itself. **Important:** GitHub browser upload may ignore the hidden `.github` folder; if so use Git or create the workflow file manually at `.github/workflows/deploy-pages.yml`.
5. Commit to `main`.
6. Go to **Settings → Pages → Build and deployment**, choose **Source: GitHub Actions**.
7. Go to **Actions**, open the deployment workflow and inspect the result. You can use **Run workflow** if it did not run automatically after enabling Pages.
8. Once deployment succeeds, the expected site URL is `https://dewawm.github.io/math-adventure-fraction-kingdom/` (your connected GitHub username is `dewawm`; the repository name must match).

## B. Upload with Git from Windows / VS Code (recommended)

Install Git, then open a terminal in the **project root** (where `package.json` is). Replace `dewawm` with your actual username, and create the empty repository via GitHub first:

```powershell
git init
git branch -M main
git add .
git commit -m "Publish Math Adventure v1.2"
git remote add origin https://github.com/dewawm/math-adventure-fraction-kingdom.git
git push -u origin main
```

Authenticate when GitHub asks. If you already have a repository with a `main` branch, do **not** force-push; fetch/merge or use a new repository.

For future changes:

```powershell
git add .
git commit -m "Update Math Adventure"
git push
```

Each push to `main` triggers a new GitHub Pages build. If you also connect Vercel, Vercel redeploys automatically on new commits.

### Option with GitHub CLI (`gh`)

After installing GitHub CLI and running `gh auth login`, you can create and publish a new repository in one operation from the project root:

```powershell
git init
git branch -M main
git add .
git commit -m "Publish Math Adventure v1.2"
gh repo create math-adventure-fraction-kingdom --public --source=. --remote=origin --push
```

Then enable GitHub Actions as the GitHub Pages publishing source in repository settings.

## C. Vercel: live game with a .vercel.app link

1. Push the source to a NEW GitHub repository (section A/B).
2. Open https://vercel.com/new and sign in.
3. Choose **Import Git Repository** and select your new `math-adventure-fraction-kingdom` repo. If it does not appear, grant Vercel GitHub App access to that repository.
4. Choose **Framework Preset: Other**, **Root Directory: ./**, **Build Command: `npm run build`**, **Output Directory: `dist`**. These settings also live in `vercel.json`.
5. Click **Deploy**. Vercel will provide the real `https://...vercel.app` URL when deployment finishes. Do not assume the URL before deployment completes.
6. Future GitHub pushes redeploy automatically via the Vercel Git integration.

**No environment variables are needed** for single-device local leaderboard, since `public/config.js` is intentionally blank.

## D. Shared online Hall of Fame (optional)

A public website does **not** automatically create a shared leaderboard! Without Supabase, scores are saved to each player's local browser (`localStorage`). To share scores between different devices:

1. Create a Supabase project at https://supabase.com.
2. Execute `supabase-schema.sql` in its SQL editor (this script is DEMO ONLY, with anonymous read/write; review privacy/security warnings).
3. Configure the public Supabase URL and **publishable/anon** key in `public/config.js`. Never place Supabase service-role or secret keys into the web project.
4. Push the update to GitHub and redeploy automatically.

**For classroom usage:** prefer aliases/initials and a private authenticated service for identifying students. Browser-submitted scores can be forged, so the demo online leaderboard is not secure enough for formal grading.

## E. Check locally before publishing

```bash
npm test
npm run build
npm run preview
```

Visit http://localhost:4173. Ensure all 3 worlds load, question blocks show quizzes, and the score screen works. Test on real mobile browsers too.

## Troubleshooting

- **404 on GitHub Pages:** confirm Pages Source is `GitHub Actions`, workflow passed, and path is `/math-adventure-fraction-kingdom/` rather than `/`.
- **404 on Vercel:** import the repository root with `package.json` and set output `dist`.
- **Black screen or broken sprites:** open browser DevTools → Network. Assets use relative `./assets/` paths and must be uploaded in their folders.
- **Git `remote origin already exists`:** run `git remote -v` before changing. Do not blindly overwrite an existing remote.
- **Leaderboard only shows current device:** expected until Supabase is configured; site hosting alone is not a shared database.
