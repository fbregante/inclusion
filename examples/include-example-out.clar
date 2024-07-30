;; <coinfabrik-auth>
;; License ...
;; CoinFabrik Libraries (v0.0.1)
(define-fungible-token auth-token u340282366920938463463374607431768211455)
(define-constant ERR_UNAUTHORIZED (err u13001))
(try! (ft-mint? auth-token u340282366920938463463374607431768211455 tx-sender))

(define-private (verify-is-owner)
    (unwrap! (ft-burn? auth-token u1 tx-sender) ERR_UNAUTHORIZED))
    
(define-public (transfer-ownership (new-owner principal))
	(unwrap! (ft-transfer? auth-token (ft-get-supply auth-token) tx-sender new-owner) ERR_UNAUTHORIZED))
;; </coinfabrik-auth>

(define-public (withdraw (amount uint))
	(let 
		((caller (tx-sender)))
		(try! (verify-is-owner)
		(as-contract (stx-transfer? amount tx-sender caller)))))
