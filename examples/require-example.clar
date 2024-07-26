;; #require(coinfabrik-utils)[BURN_BLOCKS_IN_YEAR]
;; #require(coinfabrik-math)[mul-up]

(define-read-only (rewards-per-burn-block (rewards uint))
  (/ rewards BURN_BLOCKS_IN_YEAR)    
)

