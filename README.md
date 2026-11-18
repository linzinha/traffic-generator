# traffic-generator
 
A training tool I built as a Technical Trainer to help new support engineers practice **recognizing and responding to attack traffic** on zones they controlled.
 
## Why I built it
 
New hires needed to learn to spot attack patterns and apply the right security controls, but the test zones they created in training saw almost no real traffic. The only options were to use customer tickets as examples, or using an existing CLI method to spam very obvious attack traffic at nothing.  When using customer tickets, that meant hoping for good example tickets to be in the queue at that moment in time because live data analysis is a much better learning experience than reviewing old screenshots. This tool filled that gap by generating a realistic baseline of ordinary traffic to a trainee's own test zone, mixed with periods of simulated attack traffic, so they could practice telling the two apart and responding in a safe, self-contained environment.

It is not capable of performing an actual attack because the overall volume is still quite low for that. The goal was not to stress a system but rather demonstrate a variety of traffic patterns that may look suspicious.
 
## What a trainee practiced
 
- Reading traffic analytics and logs to establish what "normal" looked like for their zone
- Spotting when a pattern shifted from ordinary traffic to a simulated attack
- Applying and tuning security controls (WAF rules, rate limiting) and confirming the effect
- Building intuition for scenario-based incident practice before handling live customer events
## Outcome
 
Used in onboarding so trainees could get hands-on detection and mitigation reps against their own zones instead of waiting for a real incident.
 
## Scope and use
 
This repository is a record of a past internal training project. It is intended only for use against systems you own or are explicitly authorized to test. It is not a general-purpose load or attack tool, and this README intentionally omits setup and operational detail.
 
## Tech
 
Python · shell
 
