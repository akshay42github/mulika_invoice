# JWT Contract — auth-service ↔ invoice-engine-service

Both services validate the same JWT independently. No network call between them at request time.

## Required claims

| Claim | Type | Meaning |
|---|---|---|
| `sub` | string | User email or user ID |
| `organization_id` | string (UUID) | Scopes all invoice-engine-service queries |
| `role` | string | `ADMIN` \| `ACCOUNTANT` \| `VIEWER` |
| `exp` | number (unix timestamp) | Token expiry |

## Signing

- Algorithm: HS256 (confirm and update here if this changes)
- Shared secret: exchanged out-of-band between Pratik and Xarvis, set as `JWT_SECRET_KEY` env var in both services
- **Never commit the secret to Git in either service**

## Open items

- [ ] Confirm token expiry duration
- [ ] Confirm refresh token strategy (if any)
- [ ] Confirm algorithm (HS256 vs RS256) — RS256 would let invoice-engine-service verify with a public key only, which is cleaner long-term
