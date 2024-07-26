;; #include(coinfabrik-auth)

(define-public (withdraw (amount uint))
	(let 
		((caller (tx-sender)))
		(try! (check-is-owner)
		(as-contract (stx-transfer? amount tx-sender caller)))))
