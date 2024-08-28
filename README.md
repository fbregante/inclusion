# Inclusion

Inclusion is a tool developed by @Coinfabrik for managing libraries in the Clarity smart contract language.


## Disclaimer

**ALWAYS review the generated code** before actually using it. 

This is an immature tool and the generated code is written in a high-level language you already know. It's not gonna take you that long.

Built-in libraries are just an example and they are not official libraries recommended as good/secure practices.


## Usage

Inclusion's preprocessor identifies directives in comments.

Directives are denoted by the prefix "#".


### Include

Include directive copy the entire library code into the contract.

Input:
```clar
;; #include(coinfabrik-utils)

(define-read-only (rewards-per-burn-block (rewards uint))
  (/ rewards BURN_BLOCKS_IN_YEAR)    
)
```

Output:
```clar
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


```


### Require

Require is a selective inclusion. Only the specified symbols (and its dependencies) will be included.

Input:
```clar
;; #require(coinfabrik-utils)[BURN_BLOCKS_IN_YEARS]

(define-read-only (rewards-per-burn-block (rewards uint))
  (/ rewards BURN_BLOCKS_IN_YEAR)    
)
```

Output:
```clar
;; <coinfabrik-utils>
(define-constant BURN_BLOCKS_IN_YEAR u52560)
;; </coinfabrik-utils>

(define-read-only (rewards-per-burn-block (rewards uint))
  (/ rewards BURN_BLOCKS_IN_YEAR)    
)
```


## Built-in Libraries

### coinfabrik-auth

Optimized solution for authentication in clarity. This keeps `tx-sender` flexibility, but enables post-condition triggering. This is achieved using FT tokens for authentication. This way, wallets in deny-mode will revert when a transaction is trying to use the authentication token.


### coinfabrik-math

Common math functions and constants which are not implemented in the standard library.


### coinfabrik-utils

Module with other utility functions.


## Roadmap

- [x] Implement `include` directive
- [x] Implement `require` directive (need TS).
- [x] Project setup and wheel dist
- [x] Code refactor
- [x] Automated test suite
- [ ] Support custom libraries
