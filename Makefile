

UNAME_S := $(shell uname -s)
UNAME_M := $(shell uname -m)
ifeq ($(UNAME_S),Darwin)
	OS_ARCH := darwin-universal
else
	ifeq ($(UNAME_M),x86_64)
		OS_ARCH := linux-amd64
	else ifeq ($(UNAME_M),arm64)
		OSARCH := linux-arm64
	endif
endif

	
bin/hugo:
	which curl || (brew install curl || apt-get install curl)
	which tar || (brew install tar || apt-get install tar)
	mkdir -p bin
	curl -L https://github.com/gohugoio/hugo/releases/download/v0.111.2/hugo_0.111.2_$(OS_ARCH).tar.gz | tar -xvzf - -C $(dir $@)

journals: $(wildcard journals/**/*)
pages: $(wildcard pages/*)
logseq: $(wildcard logseq/**/*)

content: binaries/logseq-export $(wildcard journals/*) $(wildcard pages/*) $(wildcard logseq/*)
	$< -blogFolder $@ -graphPath .

