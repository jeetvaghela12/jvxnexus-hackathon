# JvX ClientShield — Hackathon Prototype

Pre-engagement client risk screening for freelancers and small service exporters — checks a prospective client's legitimacy *before* you do unpaid work for them.

Built solo in 22 hours at the GIFT IFIH Young Builders' Program Hackathon. This is a focused prototype of the ClientShield pillar from the full [JvX Nexus](https://github.com/jeetvaghela12/JvX_Nexus) project — the piece that needs no bank partnership or license to be useful today.

## The Problem

A 2018 PayPal survey of 500 Indian freelancers found 61% had gone unpaid by a client at least once. Most fraud-screening tools check a client *after* money changes hands. ClientShield checks *before* you start work — so you can walk away from a bad client instead of chasing a bad payment.

## What It Does

- **Domain age check** — flags recently-registered domains via RDAP, no API key required
- **Business registry verification** — cross-checks UK Companies House and GLEIF LEI records
- **Email infrastructure validation** — MX record checks plus disposable-email detection
- **Threat intelligence** — Google Web Risk lookups
- **Weighted risk scoring** — combines every signal into a single LOW / MEDIUM / HIGH verdict, with the full reasoning returned alongside the score. A sanctions-list hit auto-overrides to HIGH regardless of any other signal.

## Tech Stack

- **Backend:** FastAPI
- **Dashboard:** Streamlit
- **Data sources:** RDAP, UK Companies House, GLEIF LEI, Google Web Risk

## Status

Built and working as a hackathon prototype in a 22-hour window — not yet in production.
Live demo: `https://jvxnexus-hackathon.streamlit.app/`

## Why This Exists

Freelancers currently have no fast, easy way to check whether a new client is legitimate before doing unpaid trial work for them. This tool closes that specific gap — screening happens before the money conversation starts, not after something's already gone wrong.

---

*Built solo by Jeet Vaghela at the GIFT IFIH Young Builders' Program Hackathon.*
