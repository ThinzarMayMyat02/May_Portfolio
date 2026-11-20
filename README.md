# May Myat Thinzar portfolio

A static, twelve-page portfolio with dark and light themes, a mobile menu, local technology icons and automatic achievement photo sliders.

## Open locally

Open `site/index.html` in a browser, or run this command from the project folder.

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory site
```

Visit http://127.0.0.1:8000. Press Ctrl+C to stop the server.

## Source structure

```text
build.py                    Command-line entry point and build sequence
portfolio/
  rendering.py              JSON loading and HTML template rendering
  components.py             Navigation, skills, project cards and galleries
data/
  site.json                 Shared name, profile links and navigation
  pages.json                Routes, page titles, metadata and template names
  skills.json               Explicit technology lists grouped by experience
  icons.json                Technology logos and concept SVG definitions
  projects.json             Featured project card content
  galleries.json            Photo groups, captions and excluded files
templates/
  layout.html               Shared document, header and footer
  pages/                    Editable content for each page
  components/               Reusable cards, skill tiles and photo slides
site/
  *.html                    Generated pages, ready for hosting
  projects/                 Generated project listing and detail pages
  assets/
    styles.css              Theme tokens, components and responsive layouts
    theme.js                Saved theme and theme button
    navigation.js           Mobile menu behavior
    gallery.js              Autoplay, swipe and keyboard photo navigation
    icons/                  Bundled logos and license files
    ...                     Portrait and achievement photographs
vercel.json                 Vercel configuration
```

## Build and edit

Use Python 3.8 or later. The builder uses only the Python standard library.

```sh
python3 build.py
```

The build reads data, renders page components, applies the shared layout and writes the HTML files into `site/`. It then writes `robots.txt`. Importing the Python modules does not build the site.

- Edit page text in `templates/pages/`.
- Edit shared navigation and profile links in `data/site.json`.
- Edit technology lists in `data/skills.json` and their matching icons in `data/icons.json`.
- Edit featured project summaries in `data/projects.json`. Individual project details are in `templates/pages/projects/`.
- Edit page titles, descriptions and route registration in `data/pages.json`.
- Edit photos and captions using `data/galleries.json`. Gallery filenames are sorted in ascending order. Metro's removed first photo remains excluded there.
- Update the portrait at `site/assets/may-portrait.png`.
- Edit design and browser interactions directly in `site/assets/`.

Regenerate after editing templates or data. Editing generated HTML directly will be overwritten by the next build. CSS and JavaScript changes do not require regeneration.

Each gallery advances every five seconds and pauses on hover, keyboard focus, touch or a hidden browser tab. Reduced-motion preferences disable automatic playback. Arrow keys and touch scrolling support manual photo navigation.

## Add photographs

Add web-sized images under `site/assets/`, using `oceanblue-memory` or `metro-convocation` at the start of the filename. Supported extensions are .webp, .jpg, .jpeg and .png. Add a descriptive caption in `data/galleries.json`, then run the build. Both achievement cards use the same responsive mini-slider component.

## Deploy on Vercel

1. Put the project files in a Git repository. Keep `vercel.json`, `build.py`, `portfolio/`, `data/`, `templates/` and `site/` at the repository root.
2. Import the repository into Vercel. Select **Other** as the framework preset, keep the repository root as the Root Directory and use `site` as the output directory.
3. The included `vercel.json` runs `python3 build.py` during deployment and skips dependency installation. Deploy the project.
4. Confirm the Production Branch is `main` in the project's Git settings.

Once connected, pushing to `main` automatically rebuilds the templates and data and deploys the generated site. Other branches and pull requests get preview deployments through the Vercel Git integration. A failed build is reported in Vercel's deployment logs.

The Git integration provides the build and deployment pipeline. Configuration in this repository takes effect after the repository is connected to a Vercel project. No GitHub Actions workflow or deployment token is required for this setup.

Vercel configuration documentation: https://vercel.com/docs/project-configuration/vercel-json
Git deployment documentation: https://vercel.com/docs/git

After the production domain is known, generate the sitemap with the actual HTTPS origin.

```sh
python3 build.py --origin https://YOUR-PRODUCTION-DOMAIN
```

Commit and push the generated site files. Keep supplying the origin for subsequent production builds. A build without `--origin` prepares a local preview and removes the production sitemap.

## Content still to add

The OceanBlue demo URL, CV and project screenshots have placeholders. Add the demo to the OceanBlue project template and achievement card, and update the Contact template when your CV is ready.

## Icon credits

Bundled technology logos come from Devicon 2.17.0 and Simple Icons 14.0.0. Their license files are in `site/assets/icons/`. Related technologies use their framework or vendor logos. Concepts use line icons.
