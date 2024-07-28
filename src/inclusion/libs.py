# In the future, this should be a reporsitory from which we download these official libraries.
# But, this is a simple solution for packaging the tool and share it with others.

HEADER = """
;; License ...
;; CoinFabrik Libraries (v0.0.1)
"""

LIBRARIES = {
    "coinfabrik-auth": (
        """
(define-non-fungible-token auth {user: uint, count: uint})
(define-map token-count uint uint)

(define-constant OWNER u0)
(define-constant ERR_UNAUTHORIZED (err u13001))

(try! (nft-mint? auth {user: OWNER, count: u0} tx-sender))
(map-insert user-count OWNER u0)

(define-private (check-is-owner)
    (let ((count (unwrap-panic (map-get? token-count OWNER))))
        (unwrap! (nft-burn? auth {user: OWNER, count: count} tx-sender) ERR_UNAUTHORIZED)
        (try! (nft-mint? auth {user: OWNER, count: (+ count u1)} tx-sender))
        (map-set token-count OWNER (+ count u1))
        (ok true)))
"""
    ),
    "coinfabrik-math": (
        """
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
"""
    ),
    "coinfabrik-utils": (
        """
;; (* u365 u24 u60 u60)
(define-constant SECONDS_IN_YEAR u31536000)
;; (* u10 u60)
(define-constant SECONDS_IN_BURN_BLOCK u600)
;; (/ (* 365 24 60) 10)
(define-constant BURN_BLOCKS_IN_YEAR u52560)
"""
    ),
}
