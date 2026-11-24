# Joe Mark Designs

A one-page site for Joe Mark, an architectural draftsman. It introduces his experience, the residential plans he draws, and direct ways to reach him for a free consultation.

The page is static: `index.html`, `styles.css`, and `script.js`. There is no build step and no server-side form. Call, text, and email links open the visitor’s own phone or mail app.

## Preview locally

From this folder:

```bash
python3 -m http.server 8741
```

Open `http://127.0.0.1:8741`.

## Update the phone or email

Search the project for these and change every occurrence, including the header, hero, contact section, and footer:

- Display phone: `(949) 413-9057`
- `tel:+19494139057`
- `sms:+19494139057`
- `MarkDesigns20@gmail.com`

The same values are listed in a comment at the top of `index.html`.

## Service area

No city or state is shown. Joe works with homeowners and contractors everywhere. The line in the hero, contact section, and footer is:

> Working with homeowners and contractors everywhere.

Change that phrase in those three places if the wording should be updated. Do not add a city or state unless the owner asks for one.

## Sample drawings

The SVG files in `drawings/` are original illustrative samples, not client projects and not construction documents. The page says so. `drawings/generate.py` rebuilds them if the linework needs a change:

```bash
python3 drawings/generate.py
```

The site does not need that script in order to run.

## Deploy

Push the folder as-is. Any static host can serve it from the repository root.

- **GitHub Pages:** Settings → Pages → deploy from the branch root (`/`). A `.nojekyll` file is included so Pages serves the files directly.
- **Cloudflare Pages:** set the build command to none and the output directory to `/`.
- **Vercel:** import the project with no framework and no build command.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The page |
| `styles.css` | Layout and color |
| `script.js` | Mobile menu and the plan lightbox |
| `favicon.svg` | Roofline icon |
| `drawings/*.svg` | Hero study and four blueprint sample sheets |
| `images/before.jpg`, `images/after.jpg` | Illustrative before-and-after house photos |
