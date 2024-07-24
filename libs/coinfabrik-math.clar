;; License ...
;; CoinFabrik Libraries (v0.0.1)
(define-constant ONE_IN_FIXED u100000000)
(define-constant ONE_IN_FIXED_SIGNED 100000000)
(define-constant FIXED_PRECISION u8)

(define-constant MAX_UINT u340282366920938463463374607431768211455)
(define-constant E 271828182)

(define-read-only (mul-up (x uint) (y uint))
  (/ (+ (* x y) (/ ONE_IN_FIXED u2)) ONE_IN_FIXED))

(define-read-only (div-up (x uint) (y uint))
  (/ (+ (* x ONE_IN_FIXED) (/ y u2)) y))

(define-read-only (mul-up-signed (x int) (y int))
  (/ (+ (* x y) (/ ONE_IN_FIXED_SIGNED 2)) ONE_IN_FIXED_SIGNED))

(define-read-only (div-up-signed (x int) (y int))
  (/ (+ (* x ONE_IN_FIXED_SIGNED) (/ y 2)) y))
