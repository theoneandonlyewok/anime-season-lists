# Seasonal Anime Lists for Sonarr

Ready-to-import [Sonarr](https://sonarr.tv) Custom Lists for each anime season,
built from [AniList](https://anilist.co) (the same data behind AniChart) and
mapped to the TheTVDB IDs that Sonarr can match on.

**Browse the available seasons:**
`https://theoneandonlyewok.github.io/anime-season-lists/`

Each season is a plain JSON list at a predictable URL:

```
https://theoneandonlyewok.github.io/anime-season-lists/<season>-<year>.json
```

For example: `https://theoneandonlyewok.github.io/anime-season-lists/summer-2026.json`
Seasons are `winter`, `spring`, `summer`, and `fall`.

## Importing a list into Sonarr

1. In Sonarr, go to **Settings → Import Lists** and click **+**.
2. Scroll to the **Advanced List** section and choose **Custom List**.
3. Fill in the fields:
   - **Name** — something like `Anime – Summer 2026`.
   - **List URL** — paste the season URL (the homepage has a copy button for each).
   - **Series Type** — set this to **Anime**. This matters: it tells Sonarr to use
     absolute episode numbering, which anime release groups rely on.
   - **Enable Automatic Add** — turn on to add shows automatically. Leave it off
     for the first sync if you'd rather review what would be added.
   - **Monitor** — choose your scope, e.g. *All Episodes* or *Future Episodes*.
   - **Quality Profile** and **Root Folder** — point these at your anime profile
     and anime library folder.
   - **Tags** — optional, e.g. `summer-2026`, so you can see at a glance which
     list brought a show in.
4. Click **Test** (confirms the URL is reachable and the JSON parses), then **Save**.
5. To pull shows in immediately, go to **System → Tasks** and click **Run** on
   **Import List Sync**. Otherwise Sonarr syncs on its normal interval.

Repeat for each season you want — each one is a separate Custom List pointed at
its own URL. They can all share the same root folder and quality profile.

## Tips

- **Use a dedicated anime root folder and quality profile.** Anime release naming
  conventions differ from western TV, so keeping them separate keeps both tidy.
- **Sequels aren't duplicates.** TheTVDB files later seasons under the original
  series, so a "Season 3" entry maps to the series Sonarr already knows — it adds
  or monitors the relevant season rather than creating a duplicate.
- **A few titles may be missing at first.** Brand-new shows occasionally aren't in
  the TVDB mapping database yet when a season starts. The lists are refreshed as
  those mappings appear, so re-syncing later can pick up late additions.
- **Re-sync periodically.** New shows get announced after a season's start; running
  the Import List Sync task again will catch them.

---
