;; <coinfabrik-utils>
(define-constant BURN_BLOCKS_IN_YEAR u52560)
;; </coinfabrik-utils>

(define-read-only (rewards-per-burn-block (rewards uint))
  (/ rewards BURN_BLOCKS_IN_YEAR)    
)

