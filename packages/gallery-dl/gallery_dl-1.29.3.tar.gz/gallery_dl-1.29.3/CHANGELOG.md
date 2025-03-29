## 1.29.3 - 2025-03-29
### Extractors
#### Additions
- [danbooru] add `favgroup` extractor
- [imhentai] support `hentaienvy.com` and `hentaizap.com` ([#7192](https://github.com/mikf/gallery-dl/issues/7192) [#7218](https://github.com/mikf/gallery-dl/issues/7218))
#### Fixes
- [bunkr] fix `filename` extraction ([#7237](https://github.com/mikf/gallery-dl/issues/7237))
- [deviantart:stash] fix legacy `sta.sh` links ([#7181](https://github.com/mikf/gallery-dl/issues/7181))
- [hitomi] fix extractors ([#7230](https://github.com/mikf/gallery-dl/issues/7230))
- [mangapark] fix extractors ([#4999](https://github.com/mikf/gallery-dl/issues/4999) [#5883](https://github.com/mikf/gallery-dl/issues/5883) [#6507](https://github.com/mikf/gallery-dl/issues/6507) [#6908](https://github.com/mikf/gallery-dl/issues/6908) [#7232](https://github.com/mikf/gallery-dl/issues/7232))
- [nozomi] fix extractors ([#7242](https://github.com/mikf/gallery-dl/issues/7242))
- [patreon] include subdomains in `session_id` cookie check ([#7188](https://github.com/mikf/gallery-dl/issues/7188))
- [patreon] do not match `/messages` URLs as creator ([#7187](https://github.com/mikf/gallery-dl/issues/7187))
- [pinterest] handle `story_pin_static_sticker_block` blocks ([#7251](https://github.com/mikf/gallery-dl/issues/7251))
- [sexcom] fix `gif` pin extraction ([#7239](https://github.com/mikf/gallery-dl/issues/7239))
- [skeb] make exceptions when extracting posts non-fatal ([#7250](https://github.com/mikf/gallery-dl/issues/7250))
- [zerochan] parse `JSON-LD` data ([#7178](https://github.com/mikf/gallery-dl/issues/7178))
#### Improvements
- [arcalive] extend `gifs` option
- [deviantart] support multiple images for single posts ([#6653](https://github.com/mikf/gallery-dl/issues/6653) [#7261](https://github.com/mikf/gallery-dl/issues/7261))
- [deviantart] add subfolder support ([#4988](https://github.com/mikf/gallery-dl/issues/4988) [#7185](https://github.com/mikf/gallery-dl/issues/7185) [#7220](https://github.com/mikf/gallery-dl/issues/7220))
- [deviantart] match `/gallery/recommended-for-you` URLs ([#7168](https://github.com/mikf/gallery-dl/issues/7168) [#7243](https://github.com/mikf/gallery-dl/issues/7243))
- [instagram] extract videos from `video_dash_manifest` data ([#6379](https://github.com/mikf/gallery-dl/issues/6379) [#7006](https://github.com/mikf/gallery-dl/issues/7006))
- [mangapark] support mirror domains
- [mangapark] support v3 URLs ([#2072](https://github.com/mikf/gallery-dl/issues/2072))
- [mastodon] support `/statuses` URLs ([#7255](https://github.com/mikf/gallery-dl/issues/7255))
- [sexcom] support new-style `/gifs` and `/videos` URLs ([#7239](https://github.com/mikf/gallery-dl/issues/7239))
- [subscribestar] detect redirects to `/age_confirmation_warning` pages
- [tiktok] add retry mechanism to rehydration data extraction ([#7191](https://github.com/mikf/gallery-dl/issues/7191))
#### Metadata
- [bbc] extract more metadata ([#6582](https://github.com/mikf/gallery-dl/issues/6582))
- [kemonoparty] extract `archives` metadata ([#7195](https://github.com/mikf/gallery-dl/issues/7195))
- [kemonoparty] enable `username`/`user_profile` metadata by default
- [kemonoparty:discord] always provide `channel_name` metadata ([#7245](https://github.com/mikf/gallery-dl/issues/7245))
- [sexcom] extract `date_url` metadata ([#7239](https://github.com/mikf/gallery-dl/issues/7239))
- [subscribestar] extract `title` metadata ([#7219](https://github.com/mikf/gallery-dl/issues/7219))
### Downloaders
- [ytdl] support processing inline HLS/DASH manifest data ([#6379](https://github.com/mikf/gallery-dl/issues/6379) [#7006](https://github.com/mikf/gallery-dl/issues/7006))
### Miscellaneous
- [aes] simplify `block_count` calculation
- [common] add `subdomains` argument to `cookies_check()` ([#7188](https://github.com/mikf/gallery-dl/issues/7188))
- [config] fix using the same key multiple times with `apply` ([#7127](https://github.com/mikf/gallery-dl/issues/7127))
- [tests] implement expected failures
