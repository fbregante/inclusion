;; <coinfabrik-utils>
;; License ...
;; CoinFabrik Libraries (v0.0.1)
(define-constant BURN_BLOCKS_IN_YEAR u52560)
;; </coinfabrik-utils>
;; <coinfabrik-math>
;; License ...
;; CoinFabrik Libraries (v0.0.1)
(define-read-only (mul-up (x uint) (y uint))
  (/ (+ (* x y) (/ ONE_IN_FIXED u2)) ONE_IN_FIXED))
;; </coinfabrik-math>

(define-read-only (rewards-per-burn-block (rewards uint))
  (/ rewards BURN_BLOCKS_IN_YEAR)    
)

