# subt

[![PyPI version](
  <https://badge.fury.io/py/subt.svg>
  )](
  <https://badge.fury.io/py/subt>
) [![Maintainability](
  <https://qlty.sh/badges/52679a0a-ac9e-4667-9d20-b214d89b6687/maintainability.svg>
  )](
  <https://qlty.sh/gh/eggplants/projects/subt>
) [![pre-commit.ci status](
  <https://results.pre-commit.ci/badge/github/eggplants/subt/master.svg>
  )](
  <https://results.pre-commit.ci/latest/github/eggplants/subt/master>
)

[![Code Coverage](
  <https://qlty.sh/badges/52679a0a-ac9e-4667-9d20-b214d89b6687/test_coverage.svg>
  )](
  <https://qlty.sh/gh/eggplants/projects/subt>
) [![Test](
  <https://github.com/eggplants/subt/actions/workflows/test.yml/badge.svg>
  )](
  <https://github.com/eggplants/subt/actions/workflows/test.yml>
)

[![ghcr latest](
  <https://ghcr-badge.egpl.dev/eggplants/subt/latest_tag?trim=major&label=latest>
 ) ![ghcr size](
  <https://ghcr-badge.egpl.dev/eggplants/subt/size>
)](
  <https://github.com/eggplants/subt/pkgs/container/subt>
)

Translate a subtitle file

## Install

```sh
pip install subt
# or
pipx install subt
```

## Run

<!-- markdownlint-disable MD033 -->
<details>

<summary> (Optional) Generate an example <code>.srt</code> file from <a href="https://www.youtube.com/watch?v=jNQXAC9IVRw">Me at the zoo</a> </summary>

```shellsession
$ yt-dlp 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
$ whisper-ctranslate2 'Me at the zoo [jNQXAC9IVRw].mp4'
$ cat 'Me at the zoo [jNQXAC9IVRw].srt'
1
00:00:00,000 --> 00:00:05,000
Alright, so here we are, one of the elephants.

2
00:00:05,000 --> 00:00:13,000
The cool thing about these guys is that they have really, really, really long trunks.

3
00:00:13,000 --> 00:00:16,000
And that's cool.

4
00:00:16,000 --> 00:00:19,000
And that's pretty much all there is to say.
```

</details>
<!-- markdownlint-enable MD033 -->

Then:

```shellsession
$ subt 'Me at the zoo [jNQXAC9IVRw].srt' -d ja
Saved: './Me at the zoo [jNQXAC9IVRw].translated.srt'
$ cat 'Me at the zoo [jNQXAC9IVRw].translated.srt'
1
00:00:00,000 --> 00:00:05,000
さて、ここに私たちは象の一人です。

2
00:00:05,000 --> 00:00:13,000
これらの人のクールなことは、彼らが本当に、本当に、本当に長い幹を持っているということです。

3
00:00:13,000 --> 00:00:16,000
そして、それはクールです。

4
00:00:16,000 --> 00:00:19,000
そして、それはほとんどすべてです。
```

## Help

```shellsession
$ subt -h
usage: subt [-h] [-S SERVICE] [-s LANG] [-d LANG] [-V] sub_file

Translate a subtitle file

positional arguments:
  sub_file

options:
  -h, --help     show this help message and exit
  -S SERVICE     service to translate (default: google)
  -s LANG        source language (default: auto)
  -d LANG        destination language (default: en)
  -V, --version  show program's version number and exit
```

## License

MIT
