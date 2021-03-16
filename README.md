# fetchrss -- A script for downloading RSS feeds

This is a very simple script that downloads an RSS feed and outputs it in
CSV format.

Usage:
```
python3 fetchrss.py URL [-o OUTPUT_FILE]
```

If `OUTPUT_FILE` is given and exists, only entries newer than the date of
the last modification of the file are appended to the already existing
content. This is to enable repeated calling with the same output file and
avoiding duplicates.

If `OUTPUT_FILE` is not given, the results are printed to stdout.

The output format consists of five columns: `id`, `title`, `link`, `date`,
`text`. If the text is encoded in the feed as embedded HTML, it is converted
to plain text.

## Known bugs

The script breaks if an RSS item doesn't contain the information on the date
of publication.

## Author and copyright

Written by Maciej Janicki in 2021 and released to public domain.

