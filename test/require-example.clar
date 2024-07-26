;; #require(coinfabrik-utils)[BURN_BLOCKS_IN_YEAR]

(define-read-only (rewards-per-burn-block (rewards uint))
  (/ rewards BURN_BLOCKS_IN_YEAR)    
)

