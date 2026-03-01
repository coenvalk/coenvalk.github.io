---
layout: single
author: Coen Valk
title: MERINGUEDRIVE Post-incident report 2026-02-28
excerpt:
  Response and mitigation of sev. 1 level incident that impaired my fiance's
  ability to watch Severance
category: infra
---

On 2026-02-28 my network storage device, MERINGUEDRIVE, was in a degraded state
for 9 hours, impacting 100% of customers for several hours.

## Root cause

The original outage was caused by a temporary loss of power (LOP) event in the
region containing the network box. The LOP event lasted approximately 54
minutes. after the datacenter regained power, MERINGEUDRIVE automatically turned
on, but internet had not recovered yet. Services requiring internet to check for
updates at startup entered a degraded state until MERINGUEDRIVE was cleanly
restarted with a functioning internet connection.

## Customer impact

The outage impacted all services that require internet for 100% of MERINGUEDRIVE
customers (2).

### Services impacted

- Plex media server
- File backup

## Timeline

The full outage lasted 9 hours and 8 minutes. The following is a full timeline
of events.

All times are in UTC.

|             Time | Event                                            |
| ---------------: | ------------------------------------------------ |
| 2026-02-28 18:25 | LOP event begins                                 |
| 2026-02-28 19:19 | LOP event ends                                   |
| 2026-02-28 13:19 | MERINGUEDRIVE restarts                           |
| 2026-02-28 13:21 | MERINGUEDRIVE enters degraded state              |
| 2026-03-01 05:21 | on-call alerted of outage by ~~fiance~~ customer |
| 2026-03-01 05:23 | on-call initiates remote restart                 |
| 2026-03-01 05:23 | MERINGUEDRIVE begins restart                     |
| 2026-03-01 05:23 | 2 beeps                                          |
| 2026-03-01 05:23 | 1 long beep                                      |
| 2026-03-01 05:24 | GrUmBbLllllleEEE                                 |
| 2026-03-01 05:26 | It bEEEeeP Ed again                              |
| 2026-03-01 05:26 | Tiny bleep                                       |
| 2026-03-01 05:31 | BEEEEEEEP                                        |
| 2026-03-01 05:32 | Restart complete                                 |
| 2026-03-01 05:32 | File backup restarted                            |
| 2026-03-01 05:33 | Plex recovered                                   |
| 2026-03-01 05:36 | MERINGUEDRIVE completed backlog of image backups |

## 5 Whys

### Why did the outage occur?

The outage started due to an LOP event.

### Why did services not recover after the LOP?

During startup MERINGUEDRIVE automatically attempts to connect to the internet,
which had not fully recovered yet. This caused updates and service
initialization to fail.

### Why did services not retry after internet recovered?

MERINGUEDRIVE services were not set to retry initialization.

### Why did the outage last so long?

Monitoring and alerting were not enabled for MERINGUEDRIVE, so the on-call
engineer was unaware of the situation until they were alerted of the service
outage by customers.

### Why was monitoring and service retry not enabled for this device?

The engineering team assumed that engineering would always be the first to
realize that MERINGUEDRIVE services end up in a degraded state so additional
alerting would just be noise. This incident occurred while the on-call engineer
was out of town so was not aware of the outage and subsequent degraded service
state.

## Incident repair items

### 1. Purchase uninterruptible power supply

In order to protect against LOP events, MERINGUEDRIVE and the internet router
should be connected to an uninterruptible power supply and battery backup. This
would keep MERINGUEDRIVE operational during sub 1 hour long power outages.

### 2. Enable automatic service restart when internet recovers

### 2. Add monitoring and alerting for degraded state
