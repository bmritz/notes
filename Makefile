REQUIRED := mkdir curl ls grep xargs unzip sed
$(foreach bin,$(REQUIRED),\
	$(if $(shell command -v $(bin) 2> /dev/null),,$(error Please install `$(bin)`)))


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


# logseq: $(wildcard logseq/**/*)

content: bin/logseq-export $(wildcard logseq/**/*)
	$< -blogFolder $@ -graphPath logseq

content/_index.md: bin/logseq-export logseq/pages/_index.md
	$< -blogFolder $(dir $@) -graphPath logseq
	# delete everything but _index.md and the dirs
	ls $(dir $@) | grep -v -e '_index.md' -e posts -e about -e logseq-images | xargs -I {} rm content/{}

content/posts: bin/logseq-export $(wildcard logseq/**/*)
	$< -blogFolder $@ -graphPath logseq
	# delete the _index.md file
	rm $@/_index.md


content/posts: export/publicExport.zip
	unzip -d $@ $< 
	mv $@/pages/* $@ && rm -rf $@/pages
	# grep $@ | xargs sed -i '' 's#{{< ref "/posts/#{{< ref "/posts/#g'
	sed -i '' 's#{{< ref "/pages/#{{< ref "/posts/#g' content/posts/*


serve: bin/hugo
	$< serve -D
