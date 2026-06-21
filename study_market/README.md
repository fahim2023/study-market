# StudyMarket

![StudyMarket on all devices](documentation/images/amiresponsive.png)

[StudyMarket](#) is a full-stack academic marketplace built with Django, where students buy and sell revision notes, past-paper solutions and study guides. Free users can preview a teaser of each document; the full content unlocks immediately after a secure Stripe payment.

[Click here to view the deployed site.](#)

[View the GitHub Repository](#)

---

## Table of Contents

- [Project Purpose](#project-purpose)
  - [Rationale](#rationale)
  - [Target Audience](#target-audience)
  - [Data Domain](#data-domain)
  - [Development Approach](#development-approach)
- [User Experience (UX)](#user-experience-ux)
  - [Goals and Objectives](#goals-and-objectives)
  - [User Stories](#user-stories)
  - [Wireframes](#wireframes)
- [Database Design](#database-design)
  - [ERD](#erd)
  - [Database Schema](#database-schema)
- [UI Design](#ui-design)
  - [Colour Scheme](#colour-scheme)
  - [Typography](#typography)
  - [Imagery](#imagery)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Security Features](#security-features)
- [Deployment](#deployment)
- [Testing](#testing)
  - [Automated Testing](#automated-testing)
  - [Manual Testing](#manual-testing)
  - [Validator Testing](#validator-testing)
  - [Responsiveness](#responsiveness)
- [Bugs](#bugs)
- [Future Implementations](#future-implementations)
- [Credits](#credits)

---

## Project Purpose

_(One paragraph: what the site does, the value for buyers, the value for sellers, the value for the site owner.)_

### Rationale

#### Background

_(The gap in the market this fills — why a peer-to-peer notes marketplace, not just a generic file host.)_

#### Purpose

_(Core purpose statement — should be immediately evident to a new visitor without documentation, per the assessment criteria.)_

### Target Audience

_(Buyers, sellers, admin — each with their own needs, mirroring the user stories below.)_

### Data Domain

_(Short description of the 8 models across 5 apps and how they relate — fuller detail goes in Database Design.)_

### Development Approach

_(Agile/incremental approach, GitHub Issues if used, TDD note, tech stack summary: Django, PostgreSQL, Stripe, Bootstrap 5, Heroku.)_

---

## User Experience (UX)

### Goals and Objectives

## **External user goals:**

## **Site owner goals:**

### User Stories

#### Visitor (not logged in)

| #   | User Story | Proof |
| --- | ---------- | ----- |

#### Buyer

| #   | User Story | Proof |
| --- | ---------- | ----- |

#### Seller

| #   | User Story | Proof |
| --- | ---------- | ----- |

#### Admin / Site Owner

| #   | User Story | Proof |
| --- | ---------- | ----- |

### Wireframes

_(Desktop/mobile wireframes per key page — Browse, Document Detail, Upload, Seller Dashboard, My Purchases.)_

---

## Database Design

### ERD

_(Entity Relationship Diagram image.)_

### Database Schema

| Model | Field | Type | Key | Notes |
| ----- | ----- | ---- | --- | ----- |

## **Relationships:**

---

## UI Design

The design system establishes a high-trust, structured environment for academic exchange, sitting at the intersection of minimalism and modern corporate design. The visual narrative prioritises clarity and utility so that study materials are easy to browse and digest, aiming to make the user feel organised, capable and prepared.

Three stylistic pillars guided every UI decision:

- **Functional Clarity** — generous whitespace and a rigorous grid
- **Academic Precision** — sharp typography and intentional use of borders
- **Approachable Utility** — softening the "institutional" feel with warm accents and human-centric micro-interactions

### Colour Scheme

A high-contrast palette distinguishes content navigation from transactional actions:

| Role      | Colour                               | Usage                                                                        |
| --------- | ------------------------------------ | ---------------------------------------------------------------------------- |
| Primary   | `#1A535C` (deep scholarly teal)      | Branding, headers, primary navigation — carries the "academic" weight        |
| Secondary | `#F4A261` (warm, sun-faded orange)   | Reserved exclusively for CTAs ("Buy", "Unlock", "Upload") and success states |
| Neutral   | `#F8F9FA` and surrounding cool greys | Background layering to reduce visual fatigue during long study sessions      |
| Error     | Standard red                         | Form/validation errors                                                       |
| Info      | Soft blue                            | Informational banners                                                        |

Borders throughout stay a crisp, low-opacity dark grey to define structure without adding visual bulk.

### Typography

**Inter** is the sole typeface across the whole site, chosen for maximum readability and a systematic, clean appearance.

- **Headlines** use tighter letter-spacing and bold weights to create strong hierarchy against body text
- **Body text** uses standard weight (400) with 1.5× line height, for comfortable reading of dense revision notes
- **Labels** use semibold weight with slight tracking to stay legible at small sizes (12–14px)
- **Mobile** headlines scale down by one tier to avoid awkward wrapping on small screens

### Layout, Spacing & Shape

- **Grid:** 12-column, 1280px max-width on desktop with 24px gutters; 4-column fluid grid with 16px margins on mobile
- **Spacing rhythm:** 4px/8px baseline — 24px for most component spacing, 40px for section breathing room
- **Corner radius:** 4px on standard elements (buttons, inputs, small cards), 8px on large containers, 12px on chips/status tags — a "soft" shape language balancing academic structure with marketplace approachability

### Elevation & Depth

Depth is built from low-contrast outlines and ambient shadows rather than heavy drop shadows — intended to feel like paper layered on a desk, not objects floating in space. Cards sit on a white background with a 1px border at rest, gain a subtle diffused shadow on hover (signalling interactivity), and modals/overlays use a more pronounced shadow to separate them from the page behind.

### Signature Component: Locked Content State

The single most important UI pattern on the site, since it's the visual proof of the payment-gating requirement: unpurchased document previews show a 4px backdrop blur over the content, with a centred lock icon and a "Purchase to Unlock" CTA in the secondary orange. This same locked/unlocked pairing is used consistently across the browse grid and the document detail page, so a user (or examiner) can immediately see the before/after of paying.

### Imagery

_(Source of any stock imagery used for hero/browse thumbnails, attribution — to confirm once final images are chosen.)_

---

## Features

### Navigation

### Homepage

### Browse & Filter

### Document Detail (Locked / Unlocked States)

### Upload Document

### Checkout (Stripe)

### Seller Dashboard

### My Purchases

### Reviews

### Admin Panel

_(Each gets a short description + screenshot once built.)_

---

## Technologies Used

## **Frontend:**

## **Backend:**

## **Database:**

## **Storage:**

## **Deployment:**

## **Development Tools:**

## **Validation Tools:**

## **Django Packages:**

---

## Security Features

_(Env vars, .gitignore, DEBUG handling, login_required, ownership checks, CSRF, password hashing, ORM/no direct DB access — fill in as each is implemented.)_

---

## Deployment

### Prerequisites

### Clone the Repository

```bash
git clone
cd study-market
```

### Local Development Setup

1.
2.
3.

### Deploy to Heroku

1.
2.

### Static & Media Files

_(Whitenoise for static; media file storage solution TBD — likely Cloudinary, since Heroku's filesystem isn't persistent.)_

---

## Testing

### Automated Testing

_(Test tables per app once tests are written.)_

### Manual Testing

_(User story → test → expected → actual → pass/fail table.)_

### Validator Testing

#### HTML Validation

#### CSS Validation

#### Python PEP8 Validation

#### JavaScript

#### Lighthouse

### Responsiveness

_(Chrome / Safari / Firefox × Desktop / Tablet / Mobile.)_

---

## Bugs

_(Each bug: issue, fix, before/after code, screenshot — added as they're hit and resolved.)_

---

## Future Implementations

- ***

## Credits

### Content

### Media

### Design Tools

### Code

_(Attribution for any external tutorials, docs, or library references used — required by the assignment spec.)_

### Tools & Platforms

### Acknowledgements
