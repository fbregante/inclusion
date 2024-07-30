;; <coinfabrik-auth>
;; License ...
;; CoinFabrik Libraries (v0.0.1)
(define-fungible-token auth u340282366920938463463374607431768211455)
(define-constant ERR_UNAUTHORIZED (err u13001))
(try! (ft-mint? auth u340282366920938463463374607431768211455 tx-sender))

(define-private (verify-is-owner)
    (unwrap! (ft-burn? auth u1 tx-sender) ERR_UNAUTHORIZED))
;; </coinfabrik-auth>

(define-public (withdraw (amount uint))
	(let 
		((caller (tx-sender)))
		(try! (check-is-owner)
		(as-contract (stx-transfer? amount tx-sender caller)))))
