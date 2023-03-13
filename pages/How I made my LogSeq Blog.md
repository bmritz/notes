public:: true

- The thing that I prized the most when building my site was ease of use. To encourage myself to write more, I want it to be as easy as possible to update, post, or build a new page. For this reason, I built this website on top of LogSeq, my note-taking application. [LogSeq](https://logseq.com) is an open source "knowledge graph" that stores your notes as markdown files on disk, and allows querying and bi-directional linking to connect ideas across domains. You may have heard of other tools of the same genre including [Roam Research](https://roamresearch.com) or [Obsidian](https://obsidian.md).
- Since I'm in LogSeq every day, and it gives me a markdown-editing UI I'm familiar with and comfortable with, I started to look for an easy way to publish my notes online.
- The standard options for publishing a logseq graph online are:
	- **[pengx17/logseq-publish](https://github.com/pengx17/logseq-publish)**
		- This essentially creates a "read-only" logseq experience as a static site. The github action powers [docs.logseq.com](https://docs.logseq.com) by exporting a graph into a set of static assets to deploy.
	- **[sawhney17/logseq-schrodinger](https://github.com/sawhney17/logseq-schrodinger)**
		- Logseq Schrödinger will export your graph as hugo-flavored markdown, which can be compiled into a static site with the hugo static-site generator.
-
- ## [pengx17/logseq-publish](https://github.com/pengx17/logseq-publish) builds a full-fledged interactive graph, but it is too slow to build
  
  Staying with a philosophy of "doing the simplest thing first," I decided to used the [pengx17/logseq-publish](https://github.com/pengx17/logseq-publish) action to publish a fully functional graph online. The github action worked as advertised after a first push, the github action went green, pointing me to my webpage. I excitedly open up the page to see... to see... well, 4 seconds later, the graph loads. It's got all the bells and whistles that you see on logseq - backlinks, sidebars, tooltips, etc, but at the cost of a payload size of 20+ MB and 20 seconds to load on mobile.  That's a no-go, especially for a blog.
-
- ## [sawhney17/logseq-schrodinger](https://github.com/sawhney17/logseq-schrodinger) requires a manual step
  As I went on to try out Logseq Schrödinger, found that it needed a couple things to happen: I had to manually export the data, unzip it, and put it in the right folders with Hugo. I also found that although the export played well with the PaperMod theme, it made some non-overridable assumptions in creating links to assets that locked you into a content structure that isn't compatible with several other Hugo Themes.
-
- ## Check out [bmritz/notes](https://github.com/bmritz/notes) for the work-in-progress
  This is a work in progress, but you can look at [https://github.com/bmritz/notes](https://github.com/bmritz/notes) for the latest efforts to publish a static site.
-