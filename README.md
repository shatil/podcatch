# PodCatch
PodCatch helps you download podcasts. I wrote it to save MP3's from NPR's _Wow
in the World_ podcast onto a thumb drive.

For now, it'll just tell you what it did and `print` invocations of `curl`.

```
python3 podcatcher.py https://link/to/your/podcast/rss/feed
```

While I just pipe the above into `bash`, I recommend editing the `print` line
at the bottom to your needs and using a download manager.

## Compatible Feeds
The following RSS feeds for shows work just fine:

* _Masters of Scale_: https://rss.art19.com/masters-of-scale
* _Story Pirates_: https://feeds.gimletmedia.com/StoryPirates?format=xml
* _Wow in the World_: https://www.npr.org/rss/podcast.php?id=510321
