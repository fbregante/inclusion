;; License ...
;; CoinFabrik Libraries (v0.0.1)
(define-non-fungible-token auth {user: uint, count: uint})
(define-map token-count uint uint)

(define-constant OWNER u0)
(define-constant ERR_NO_OWNER (err 13001))

(nft-mint? auth {user: OWNER, count: u0} tx-sender)
(map-insert user-count OWNER u0)

(define-private (check-is-owner)
    (let (count (unwrap-panic (map-get? auth OWNER)))
        (nft-burn? auth {user: OWNER, count: count} tx-sender)
        (nft-mint? auth {user: OWNER, count: (+ count u1)} tx-sender)
        (map-set auth OWNER (+ count u1))
        (ok true)))
