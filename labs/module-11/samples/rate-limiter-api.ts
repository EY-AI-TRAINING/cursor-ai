// rate-limiter.ts — sample module for the focused subagent test
// Read-only fixture for Lab 11.3. The subagent must summarize the PUBLIC API surface
// using only this file — no other context from the parent agent.

export interface RateLimitDecision {
  allowed: boolean;
  remaining: number;
  retryAfterSeconds?: number;
}

export interface RateLimitConfig {
  requestsPerMinute: number;
  windowSeconds: number;
}

export function configureLimit(config: Partial<RateLimitConfig>): void;

export function checkRateLimit(apiKey: string, now?: Date): RateLimitDecision;

export function getRemaining(apiKey: string): number;

export function resetLimits(): void; // test-only helper, documented as not for production use

// Non-exported internals: slidingWindow(), bucketKey(), pruneExpired()
