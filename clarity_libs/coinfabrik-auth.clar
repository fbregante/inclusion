;; License ...
;; CoinFabrik Libraries (v0.0.1)
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
