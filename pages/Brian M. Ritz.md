- I'm Brian. I'm a Catholic, Husband, Father, and the Director of Data Science Solutions at [SPINS](https://spins.com).
-
- ## Posts
  #+BEGIN_QUERY
  {
   :query [:find (pull ?p [*])
  		:where
  			[?p :block/name _]
              [?p :page/journal? false]
              [?p :block/file _]
  		]
   :table-view? true
  :result-transform (fn [result]
                        (sort-by (fn [h]
                                   (- (get h :block/created-at))) result))
  }
  #+END_QUERY
- ## Journal Entries
  #+BEGIN_QUERY
  {
   :query [:find (pull ?p [*])
  		:where
  			[?p :block/name _]
              [?p :page/journal? true]
  		]
   :table-view? true
  }
  #+END_QUERY
-