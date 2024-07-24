;; <coinfabrik-utils>
;; License ...
;; CoinFabrik Libraries (v0.0.1)
;; (* u365 u24 u60 u60)
(define-constant SECONDS_IN_YEAR u31536000)
;; (* u10 u60)
(define-constant SECONDS_IN_BURN_BLOCK u600)
;; (/ (* 365 24 60) 10)
(define-constant BURN_BLOCKS_IN_YEAR u52560)
;; </coinfabrik-utils>

(define-read-only (rewards-per-burn-block (rewards uint))
  (/ rewards BURN_BLOCKS_IN_YEAR)    
)

