# StudyMarket

![StudyMarket on all devices](documentation/images/amiresponsive.png)

[StudyMarket](#) is a full-stack academic marketplace built with Django, where students buy and sell revision notes, past-paper solutions and study guides. Free users can preview a teaser of each document; the full content unlocks immediately after a secure Stripe payment.

[Click here to view the deployed site.](https://study-market-fahim-70194c90b021.herokuapp.com/)

[View the GitHub Repository](https://github.com/fahim2023/study-market.git)

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
  - [Layout Spacing and Shape](#layout-spacing-and-shape)
  - [Elevation and Depth](#elevation-and-depth)
  - [Signature Component Locked Content State](#signature-component-locked-content-state)
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
- [Design Decisions](#design-decisions)
- [Future Implementations](#future-implementations)
- [Credits](#credits)

---

## Project Purpose

StudyMarket is a full-stack peer-to-peer academic marketplace built with Django, where students buy and sell revision notes, past-paper solutions and study guides. The platform solves a real problem in the student market: high-quality revision materials exist in abundance but are scattered across informal channels with no quality control, no payment infrastructure and no discoverability. StudyMarket brings these materials into a structured, searchable marketplace with a secure Stripe payment flow at its core.

For **buyers**, the value is immediate — they can browse a curated catalog of subject-specific study materials, preview enough content to judge quality before committing, and gain instant access to a full document the moment payment is confirmed. The content gating is the central mechanic of the platform: every document shows a title, subject badge, seller name, price and a written preview snippet to all visitors, but the full content and download link are locked behind a Stripe payment. This ensures buyers can make an informed decision without being able to derive the full value for free.

For **sellers**, the value is passive income from work they have already done. A student who has spent hours creating revision notes for their own A-Level Biology exam can upload those notes once, set a price, and earn money every time another student purchases them — without any additional effort. The seller dashboard gives them full control over their listings: upload, edit, delete and monitor their catalog from a single page.

For the **site owner**, the value is a scalable platform that facilitates transactions between students while maintaining catalog quality through an admin-curated subject taxonomy, a purchase-gated review system and Django admin oversight of all listings, purchases and reviews.

---

### Rationale

#### Background

Revision notes and past-paper solutions have always been shared informally between students — passed around in WhatsApp groups, uploaded to Google Drive folders, or sold individually on social media. These channels are unstructured, impossible to search, and offer no quality assurance or payment protection. A buyer has no way to preview content before paying, no recourse if the material is poor quality, and no guarantee of instant delivery.

Generic file hosting platforms such as Dropbox or Google Drive lack any marketplace functionality — there is no browsing by subject, no payment mechanism, no seller reputation system and no content gating to protect sellers' intellectual property. Platforms like Scribd exist but operate on a subscription model that does not reward individual student sellers, are not tailored to the UK academic curriculum (GCSE, A-Level, undergraduate level), and do not provide the preview-then-unlock experience that makes the value proposition immediately clear to a new user.

StudyMarket fills this gap by combining four things that no existing platform does together: a structured, searchable catalog of UK-curriculum academic materials; a per-document Stripe payment flow with instant access on success; a seller dashboard with full CRUD over listings; and a purchase-gated review system that ensures only verified buyers can leave feedback. The result is a trustworthy marketplace where both sides of the transaction — buyer and seller — have clear, protected incentives.

#### Purpose

The core purpose of StudyMarket is to make high-quality, peer-created revision materials discoverable and accessible to students who need them, while rewarding the students who created them. This purpose is immediately evident to a new visitor without any documentation: the homepage hero states "Get exam-ready notes from students who've already aced the course", the browse page shows a grid of subject-tagged documents with prices and previews, and every document detail page makes the locked/unlocked distinction visually explicit — a blurred content card with a lock icon and "Unlock for £X" CTA for unpurchased documents, replaced by a green "You have access" card with a download button after payment.

The payment-gating mechanic is the single most important feature of the platform and the primary reason a regular user cannot derive the full value of the site without paying. It is implemented at two levels: the `document_detail` view checks the `Purchase` model before deciding which template block to render, and a Stripe webhook provides a server-side backup that records purchases even if a buyer closes their browser before reaching the success page.

---

### Target Audience

**Buyers — students preparing for exams**

The primary buyer is a student at GCSE, A-Level or undergraduate level who is preparing for upcoming exams and needs high-quality revision materials quickly. They are time-poor and willing to pay a small fee (typically £3–£15) to save significant study time. They need to be able to find materials relevant to their specific subject and level, preview enough content to judge quality before committing to a purchase, trust that the payment process is secure, and receive instant access to the document the moment payment is confirmed. They may also want to leave a review after purchasing to help future buyers make informed decisions.

**Sellers — students monetising their existing notes**

The seller is typically a student who has recently completed a course — or is currently studying it — and has already created detailed revision notes for their own use. They want to earn passive income from work they have already done, with minimal effort. They need a simple, reliable upload flow where they can set a title, select the relevant course, write a preview and set a price. They need confidence that their full content is protected behind a payment wall so they are not giving away their work for free. They also need control over their listings — the ability to edit details or remove listings if the material becomes outdated.

**Admins and site owners — platform curators**

The admin is responsible for maintaining the quality and integrity of the platform. They curate the subject and course taxonomy through the Django admin panel, ensuring that the catalog remains well-organised and free of duplicates. They can moderate listings and reviews where necessary, monitor all purchase activity, and manage user accounts. The admin role also encompasses the site owner's commercial interest — ensuring that the payment-gating mechanic is watertight, that no user can access full content without paying, and that the Stripe integration is functioning correctly in production.

---

### Data Domain

StudyMarket's data is organised across 8 custom models in 5 Django apps. At the centre is the `Document` model, which belongs to a `Course` (itself grouped under a `Subject`) and is uploaded by a seller (`auth.User`). When a buyer purchases a document, a `Purchase` record is created linking that user to that document — this is the access control mechanism of the entire platform. Buyers who have a `Purchase` record can leave a `Review`. Each user also has a `Profile` (created automatically via signal) which stores whether they are a seller. `DocumentTag` provides a many-to-many tagging system for filtering. Full detail in the [Database Schema](#database-schema) section below.

---

### Development Approach

StudyMarket was built incrementally using an agile approach — one feature at a time, committed to git at natural feature-complete boundaries, and deployed to Heroku after each commit. No feature was considered done until it passed a `python manage.py check`, worked locally in the browser, and was verified on the live Heroku site.

Test-Driven Development was applied to the model and view layer: automated tests were written alongside or immediately after each new model, catching regressions before they reached production. All test runs use a local SQLite database to avoid conflicts with Neon's connection pooling (see Bug 4).

**Tech stack summary:** Django 5.2 · PostgreSQL (Neon) · Stripe · Bootstrap 5 · Cloudinary · Heroku · Whitenoise · Git/GitHub

---

## User Experience (UX)

### Goals and Objectives

**External user goals:**

- Browse and discover high-quality revision materials by subject and level without needing to register
- Preview document content before committing to a purchase
- Purchase documents securely via Stripe and gain instant access
- Upload and sell their own study materials with full control over pricing and listings
- Leave and manage reviews on purchased documents

**Site owner goals:**

- Provide a trustworthy marketplace where buyers cannot access full document content without paying
- Maintain a well-organised, admin-curated subject taxonomy
- Monitor all purchases and reviews through the Django admin panel
- Ensure the platform is secure, with no credentials exposed and all sensitive actions requiring authentication

---

### User Stories

#### Visitor (not logged in)

| #   | User Story                                                                                                      | Proof                                                              |
| --- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| 1   | As a visitor I can browse all published documents so I can see what's on offer before registering               | Browse page accessible without login                               |
| 2   | As a visitor I can view a document's title, course, price and preview text so I can decide if it's worth buying | Document detail page shows preview to all users                    |
| 3   | As a visitor I cannot view the full document content or download it until I have paid                           | Locked content card shown to unauthenticated and unpurchased users |
| 4   | As a visitor I can register an account so I can buy or sell documents                                           | `/accounts/register/`                                              |
| 5   | As a visitor I can log in so I can access my purchases                                                          | `/accounts/login/`                                                 |

#### Buyer

| #   | User Story                                                                         | Proof                                                       |
| --- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| 6   | As a buyer I can search documents by keyword so I can find relevant notes quickly  | Search bar on browse page filters by title                  |
| 7   | As a buyer I can filter documents by subject so I can narrow results to my course  | Subject radio filter on browse sidebar                      |
| 8   | As a buyer I can purchase a document via Stripe so I get full access to it         | Stripe checkout at `/payments/checkout/<id>/`               |
| 9   | As a buyer I receive clear confirmation after a successful payment                 | Payment success page rendered after Stripe confirms payment |
| 10  | As a buyer I can view and download any document I have purchased from My Purchases | My Purchases page at `/payments/my-purchases/`              |
| 11  | As a buyer I can leave a rating and review on a document I have purchased          | Add review form gated behind purchase check                 |
| 12  | As a buyer I cannot review a document I have not purchased                         | `add_review` view redirects unpurchased users               |
| 13  | As a buyer I can edit my review if I change my mind                                | Edit review view at `/reviews/edit/<id>/`                   |
| 14  | As a buyer I can delete my review                                                  | Delete review view at `/reviews/delete/<id>/`               |

#### Seller

| #   | User Story                                                                                  | Proof                                                                            |
| --- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| 15  | As a seller I can upload a new document with title, description, price, course and PDF file | Upload form at `/documents/seller/upload/`                                       |
| 16  | As a seller I can see all my listings on a dashboard so I can manage them                   | Seller dashboard at `/documents/seller/dashboard/`                               |
| 17  | As a seller I can edit my own listings                                                      | Edit document view at `/documents/seller/edit/<slug>/`                           |
| 18  | As a seller I can delete my own listings                                                    | Delete document view at `/documents/seller/delete/<slug>/`                       |
| 19  | As a seller I cannot edit or delete another seller's listings                               | `get_object_or_404(Document, slug=slug, seller=request.user)` enforces ownership |

#### Admin / Site Owner

| #   | User Story                                                                                        | Proof                                                               |
| --- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| 20  | As an admin I can manage subjects and courses so the catalog stays organised                      | Subject and Course models registered in Django admin                |
| 21  | As an admin I can view all purchases so I can monitor sales activity                              | Purchase model registered in admin with list display                |
| 22  | As an admin I can moderate reviews if needed                                                      | Review model registered in admin                                    |
| 23  | As a site owner there is no way for a regular user to access full document content without paying | Purchase check in `document_detail` view; webhook backup via Stripe |

---

### Wireframes

_(Desktop/mobile wireframes per key page — Browse, Document Detail, Upload, Seller Dashboard, My Purchases.)_

---

## Database Design

### ERD

_(Entity Relationship Diagram image — to be added once finalised.)_

---

### Database Schema

The database consists of 8 custom models across 5 Django apps. All models use Django's default `BigAutoField` as the primary key unless otherwise noted.

---

#### `accounts` app

**Profile**

| Field         | Type                        | Key | Constraints               | Notes                                         |
| ------------- | --------------------------- | --- | ------------------------- | --------------------------------------------- |
| `id`          | BigAutoField                | PK  | Auto, unique              | Django default primary key                    |
| `user`        | OneToOneField → `auth.User` | FK  | Unique, CASCADE on delete | Links profile to Django's built-in User model |
| `is_seller`   | BooleanField                |     | Default: False            | Distinguishes buyers from sellers             |
| `bio`         | TextField                   |     | Blank, null               | Optional seller biography                     |
| `institution` | CharField(100)              |     | Blank, null               | University or school name                     |

**Relationships:**

- `Profile.user` → `auth.User` (OneToOne) — created automatically via signal on user registration. Cascade delete ensures the profile is removed when the user account is deleted.

---

#### `courses` app

**Subject**

| Field  | Type           | Key | Constraints            | Notes                                       |
| ------ | -------------- | --- | ---------------------- | ------------------------------------------- |
| `id`   | BigAutoField   | PK  | Auto, unique           | Django default primary key                  |
| `name` | CharField(100) |     | Unique                 | e.g. Biology, Mathematics, Law              |
| `slug` | SlugField(120) |     | Unique, auto-generated | URL-safe version of name, generated on save |

**Course**

| Field        | Type                   | Key | Constraints                           | Notes                                          |
| ------------ | ---------------------- | --- | ------------------------------------- | ---------------------------------------------- |
| `id`         | BigAutoField           | PK  | Auto, unique                          | Django default primary key                     |
| `subject`    | ForeignKey → `Subject` | FK  | CASCADE on delete                     | Groups courses under a subject area            |
| `name`       | CharField(200)         |     |                                       | e.g. A-Level Biology, GCSE Mathematics         |
| `level`      | CharField(20)          |     | Choices: gcse, a_level, undergraduate | Academic level of the course                   |
| `exam_board` | CharField(50)          |     | Blank, null                           | e.g. AQA, Edexcel, OCR                         |
| `slug`       | SlugField(250)         |     | Unique, auto-generated                | Generated from subject, name and level on save |

**Relationships:**

- `Course.subject` → `Subject` (ForeignKey, CASCADE) — a Subject can have many Courses. Deleting a Subject cascades to all its Courses.

---

#### `documents` app

**Document**

| Field          | Type                     | Key | Constraints                               | Notes                                             |
| -------------- | ------------------------ | --- | ----------------------------------------- | ------------------------------------------------- |
| `id`           | BigAutoField             | PK  | Auto, unique                              | Django default primary key                        |
| `title`        | CharField(200)           |     |                                           | Document listing title                            |
| `seller`       | ForeignKey → `auth.User` | FK  | CASCADE on delete                         | The user who uploaded this document               |
| `course`       | ForeignKey → `Course`    | FK  | CASCADE on delete                         | The course this document belongs to               |
| `description`  | TextField                |     |                                           | Full description shown after purchase             |
| `preview_text` | TextField                |     |                                           | Short teaser visible to all users before purchase |
| `file`         | FileField                |     | Upload to `documents/`                    | The PDF file stored on Cloudinary in production   |
| `price`        | DecimalField(6,2)        |     |                                           | Price in GBP                                      |
| `status`       | CharField(10)            |     | Choices: draft, published; Default: draft | Only published documents appear in browse         |
| `slug`         | SlugField(250)           |     | Unique, auto-generated                    | Generated from title on save                      |
| `created_at`   | DateTimeField            |     | Auto now add                              | Timestamp of upload                               |
| `updated_at`   | DateTimeField            |     | Auto now                                  | Timestamp of last edit                            |

**DocumentTag**

| Field       | Type                         | Key | Constraints  | Notes                                 |
| ----------- | ---------------------------- | --- | ------------ | ------------------------------------- |
| `id`        | BigAutoField                 | PK  | Auto, unique | Django default primary key            |
| `name`      | CharField(50)                |     | Unique       | e.g. exam-style, summary, diagrams    |
| `documents` | ManyToManyField → `Document` | M2M |              | Tags can be applied to many documents |

**Relationships:**

- `Document.seller` → `auth.User` (ForeignKey, CASCADE) — a User can sell many Documents. Deleting a User cascades to all their Documents.
- `Document.course` → `Course` (ForeignKey, CASCADE) — a Course can have many Documents. Deleting a Course cascades to all its Documents.
- `DocumentTag.documents` → `Document` (ManyToMany) — a Tag can be applied to many Documents and a Document can have many Tags. Django creates a join table automatically.

---

#### `payments` app

**Purchase**

| Field                   | Type                     | Key | Constraints       | Notes                                     |
| ----------------------- | ------------------------ | --- | ----------------- | ----------------------------------------- |
| `id`                    | BigAutoField             | PK  | Auto, unique      | Django default primary key                |
| `buyer`                 | ForeignKey → `auth.User` | FK  | CASCADE on delete | The user who made the purchase            |
| `document`              | ForeignKey → `Document`  | FK  | CASCADE on delete | The document that was purchased           |
| `stripe_payment_intent` | CharField(200)           |     | Unique            | Stripe PaymentIntent ID (`pi_...`)        |
| `amount_paid`           | DecimalField(6,2)        |     |                   | Amount charged in GBP at time of purchase |
| `created_at`            | DateTimeField            |     | Auto now add      | Timestamp of purchase                     |

**Constraints:**

- `unique_together = ('buyer', 'document')` — prevents a user from purchasing the same document twice

**Relationships:**

- `Purchase.buyer` → `auth.User` (ForeignKey, CASCADE) — a User can have many Purchases. Deleting a User cascades to all their Purchase records.
- `Purchase.document` → `Document` (ForeignKey, CASCADE) — a Document can have many Purchases. Deleting a Document cascades to all related Purchase records.
- The `Purchase` model is the access control mechanism of the platform — the `document_detail` view checks for a `Purchase` record before deciding whether to render the locked or unlocked content state.

---

#### `reviews` app

**Review**

| Field        | Type                     | Key | Constraints       | Notes                        |
| ------------ | ------------------------ | --- | ----------------- | ---------------------------- |
| `id`         | BigAutoField             | PK  | Auto, unique      | Django default primary key   |
| `document`   | ForeignKey → `Document`  | FK  | CASCADE on delete | The document being reviewed  |
| `reviewer`   | ForeignKey → `auth.User` | FK  | CASCADE on delete | The user leaving the review  |
| `rating`     | IntegerField             |     | Choices: 1–5      | Star rating                  |
| `comment`    | TextField                |     |                   | Written review body          |
| `created_at` | DateTimeField            |     | Auto now add      | Timestamp of review creation |
| `updated_at` | DateTimeField            |     | Auto now          | Timestamp of last edit       |

**Constraints:**

- `unique_together = ('document', 'reviewer')` — prevents a user from reviewing the same document twice

**Relationships:**

- `Review.document` → `Document` (ForeignKey, CASCADE) — a Document can have many Reviews. Deleting a Document cascades to all its Reviews.
- `Review.reviewer` → `auth.User` (ForeignKey, CASCADE) — a User can write many Reviews. Deleting a User cascades to all their Reviews.
- Reviews are purchase-gated at the view level — the `add_review` view checks for a `Purchase` record with matching `buyer` and `document` before allowing a review to be submitted.

---

### Relationships Summary

```
auth.User
    │
    ├──(OneToOne)──▶ Profile
    │
    ├──(FK, seller)──▶ Document
    │                       │
    │                       ├──(FK)──▶ Course ──(FK)──▶ Subject
    │                       │
    │                       ├──(M2M)──▶ DocumentTag
    │                       │
    │                       ├──(FK)──▶ Purchase ◀──(FK, buyer)── auth.User
    │                       │
    │                       └──(FK)──▶ Review ◀──(FK, reviewer)── auth.User
    │
    └──(FK, buyer)──▶ Purchase
```

**Key access control chain:**
`auth.User` → `Purchase` → `Document` — a user can only access the full content of a Document if a Purchase record exists linking their User account to that Document.

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
| Secondary | `#8e4e14` (warm amber-brown)         | Reserved exclusively for CTAs ("Buy", "Unlock", "Upload") and success states |
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

### Layout, Spacing and Shape

- **Grid:** 12-column, 1280px max-width on desktop with 24px gutters; 4-column fluid grid with 16px margins on mobile
- **Spacing rhythm:** 4px/8px baseline — 24px for most component spacing, 40px for section breathing room
- **Corner radius:** 4px on standard elements (buttons, inputs, small cards), 8px on large containers, 12px on chips/status tags — a "soft" shape language balancing academic structure with marketplace approachability

### Elevation and Depth

Depth is built from low-contrast outlines and ambient shadows rather than heavy drop shadows — intended to feel like paper layered on a desk, not objects floating in space. Cards sit on a white background with a 1px border at rest, gain a subtle diffused shadow on hover (signalling interactivity), and modals/overlays use a more pronounced shadow to separate them from the page behind.

### Signature Component: Locked Content State

The single most important UI pattern on the site, since it's the visual proof of the payment-gating requirement: unpurchased document previews show a backdrop blur over the content, with a centred lock icon and a "Purchase to Unlock" CTA in the secondary amber. This same locked/unlocked pairing is used consistently across the browse grid and the document detail page, so a user (or examiner) can immediately see the before/after of paying.

### Imagery

Subject-specific photography is used for document card thumbnails throughout the browse page and homepage featured section. Images were generated using Google ImageFX with prompts designed to match the teal/amber colour palette of the site. Images used:

- `hero_image.png` — laptop on teal desk, hero section
- `biology.png` — biology textbooks and microscope on teal surface
- `economics.png` — economics textbook with charts and graphs
- `history.png` — vintage maps and handwritten notes on teal desk
- `law.png` — open law textbook with case notes
- `math.png` — mathematics notebook with equations and calculator
- `psychology.png` — psychology textbooks with brain diagrams
- `general.png` — general study notes and sticky notes on teal desk

---

## Features

| #   | Feature                        | Description                                                                                                                                                                                                                                                                                                                                                                                                   | Screenshot                                                                                         |
| --- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| 1   | **Navigation**                 | Sticky navbar on every page. Anonymous users see Browse, search bar, Log in and Register. Authenticated users see Browse, Sell, My Purchases, username and Log out. Collapses to a hamburger menu on mobile. Logo links to homepage from any page.                                                                                                                                                            | ![Navigation](documentation/images/features/feature-01-homepage.png)                               |
| 2   | **Homepage**                   | Multi-section landing page making the platform purpose immediately evident. Sections: hero with headline and CTAs; Explore by Subject grid with Bootstrap Icons; Featured Revision Guides showing 6 most recent documents with subject images, ratings and prices; How StudyMarket Works with contrasting buyer/seller cards; CTA strip. Purchased documents show without the locked overlay.                 | ![Homepage](documentation/images/features/feature-01-homepage.png)                                 |
| 3   | **Browse**                     | Full document catalog with left sidebar filter panel and responsive 3-column grid. Each card shows subject thumbnail, locked overlay for unpurchased documents, subject badge, course level, title, seller name, star rating and price. Purchased documents show a View button instead of Buy Now with no locked overlay.                                                                                     | ![Browse](documentation/images/features/feature-02-browse.png)                                     |
| 4   | **Filter by Subject**          | Sidebar radio buttons filter the catalog by subject. Filter persists across pagination and combines with sort. Clear filter link removes the active filter.                                                                                                                                                                                                                                                   | ![Browse filtered](documentation/images/features/feature-03-browse-filtered.png)                   |
| 5   | **Sort**                       | Bootstrap dropdown in sidebar to sort documents by Most Recent, Price Low to High, Price High to Low, A–Z, Z–A or Top Rated. Sort value persists across pagination and combines with subject filter.                                                                                                                                                                                                          | ![Browse sorted](documentation/images/features/feature-04-browse-sorted.png)                       |
| 6   | **Document Detail — Locked**   | Unauthenticated users and users who have not purchased see a locked content card with a lock icon and Unlock for £X CTA. The full document content, description and download link are not accessible. Anonymous users see a Log in to purchase button.                                                                                                                                                        | ![Document detail locked](documentation/images/features/feature-05-document-detail-locked.png)     |
| 7   | **Document Detail — Unlocked** | Users who have purchased see a green "You have access" card with the full description and a Download Document button. The sidebar also shows a Download button. This locked/unlocked pairing is the core mechanic of the platform and is visually clear to any examiner.                                                                                                                                      | ![Document detail unlocked](documentation/images/features/feature-06-document-detail-unlocked.png) |
| 8   | **Reviews**                    | Reviews section on the document detail page shows all reviews with reviewer username, date, star rating rendered as filled/empty stars and comment. Edit and Delete buttons visible only to the review author. Write a Review button shown only to buyers who have purchased but not yet reviewed.                                                                                                            | ![Reviews](documentation/images/features/feature-07-reviews.png)                                   |
| 9   | **Stripe Checkout**            | Secure Stripe card input element (card number, expiry, CVC — postal code hidden for UK compatibility). On submission a POST fetches a PaymentIntent `client_secret` from the server. `checkout.js` calls `stripe.confirmCardPayment()` to process the payment client-side. A Stripe webhook at `/payments/webhook/` provides server-side backup purchase recording verified using the webhook signing secret. | ![Checkout](documentation/images/features/feature-08-checkout.png)                                 |
| 10  | **Payment Success**            | Success page rendered after Stripe confirms payment. Purchase record is created in the database giving the buyer permanent access to the document. Clear confirmation message shown to the user.                                                                                                                                                                                                              | ![Payment success](documentation/images/features/feature-09-payment-success.png)                   |
| 11  | **My Purchases**               | Grid of all documents purchased by the logged-in buyer. Each card shows subject thumbnail, subject badge, title, seller name, View Now and PDF download buttons. A Leave a Review button appears for documents not yet reviewed. Subject filter in the sidebar narrows the library. Empty state shown with Browse Notes CTA when no purchases exist.                                                          | ![My Purchases](documentation/images/features/feature-10-my-purchases.png)                         |
| 12  | **Seller Dashboard**           | Table of all documents uploaded by the logged-in seller. Each row shows title, subject badge, price, published/draft status badge, upload date and icon action buttons — eye (view), pencil (edit), trash (delete). Empty state shown with Upload CTA. Sellers can only manage their own documents.                                                                                                           | ![Seller Dashboard](documentation/images/features/feature-11-seller-dashboard.png)                 |
| 13  | **Upload Document**            | Seller upload form with title, course dropdown, price, preview text, full description, PDF file upload and draft/published status. File size validated server-side — files over 10MB rejected with a clear error message before Cloudinary upload is attempted.                                                                                                                                               | ![Upload](documentation/images/features/feature-12-upload.png)                                     |
| 14  | **Add Review**                 | Write a Review form with radio-button star rating (1–5) and comment textarea. Only accessible to buyers who have purchased the document and not yet reviewed it. Users who have not purchased are redirected away.                                                                                                                                                                                            | ![Add Review](documentation/images/features/feature-13-add-review.png)                             |
| 15  | **Register**                   | Custom register page with StudyMarket logo badge, username, email, password and password confirmation fields. Help text removed for a clean UI. Only accessible to anonymous users — authenticated users are redirected to homepage.                                                                                                                                                                          | ![Register](documentation/images/features/feature-14-register.png)                                 |
| 16  | **Login**                      | Custom login page with StudyMarket logo badge, username and password fields, and social proof stats (10k+ verified notes, 4.9/5 avg rating). Only accessible to anonymous users. After successful login users are redirected to the homepage.                                                                                                                                                                 | ![Login](documentation/images/features/feature-15-login.png)                                       |
| 17  | **Auto-dismiss Alerts**        | Success and error messages (e.g. "Your document has been updated", "Welcome back") auto-dismiss after 3 seconds with a fade-out transition, implemented in `static/js/alerts.js`.                                                                                                                                                                                                                             | ![Alerts](documentation/images/features/feature-01-homepage.png)                                   |
| 18  | **Custom 404 Page**            | Custom `404.html` extending `base.html`, showing a friendly "Page Not Found" message with a Back to Home button. Served automatically by Django when `DEBUG=False` on Heroku.                                                                                                                                                                                                                                 | ![404](documentation/images/features/feature-16-404.png)                                           |
| 19  | **Django Admin Panel**         | Admin registered for all models: Subject, Course, Document, DocumentTag, Purchase, Review and Profile. Each has `list_display`, `list_filter` and `search_fields` configured. Sole interface for managing the subject and course taxonomy.                                                                                                                                                                    | ![Admin](documentation/images/features/feature-17-admin.png)                                       |

## Technologies Used

### Frontend

- **HTML5** — semantic markup used throughout all templates to convey structure and support accessibility
- **CSS3** — custom design system built in `static/css/style.css`, implementing the StudyMarket brand palette, typography scale, component styles and responsive breakpoints
- **Bootstrap 5.3** — responsive grid system, utility classes, navbar, cards, forms, badges and pagination components, loaded via CDN
- **Bootstrap Icons 1.11** — icon library used for subject icons, how-it-works step icons and UI affordances, loaded via CDN
- **JavaScript (ES6+)** — custom JS written in `payments/static/payments/js/checkout.js` to handle the Stripe payment flow: fetching the PaymentIntent client secret via POST, mounting the Stripe card element, confirming payment and redirecting on success
- **Stripe.js v3** — Stripe's official JavaScript library loaded from `https://js.stripe.com/v3/`, used to create the secure card input element and confirm card payments client-side
- **Google Fonts (Inter)** — loaded via `<link>` in `base.html`, used as the sole typeface across the entire site for maximum readability and a clean, systematic appearance

### Backend

- **Python 3.12** — primary programming language
- **Django 5.2 LTS** — full-stack web framework providing the ORM, URL routing, template engine, authentication system, admin panel, form validation and management commands
- **Stripe Python SDK (`stripe==15.2.1`)** — used server-side in `payments/views.py` to create PaymentIntents and in `stripe_webhook` to verify and process incoming webhook events
- **Gunicorn** — WSGI HTTP server used to serve the Django application in production on Heroku

### Database

- **PostgreSQL** — relational database used in both development and production, hosted on **Neon** (serverless Postgres). Connected via `dj-database-url` which parses the `DATABASE_URL` environment variable into Django's `DATABASES` setting
- **SQLite** — used exclusively during automated test runs to avoid conflicts between Django's test database create/destroy cycle and Neon's connection pooling (see Bug 4)

### Storage

- **Cloudinary** — cloud media storage used in production to persist user-uploaded PDF files across Heroku dyno restarts. Configured via `django-cloudinary-storage` using the `STORAGES['default']` backend
- **Whitenoise 6.12** — serves compressed, hashed static files (CSS, JS, images) directly from Django in production without requiring a separate static file server. Configured as the `STORAGES['staticfiles']` backend

### Deployment

- **Heroku** — cloud platform used to host the production application. Configured with a `Procfile` declaring the Gunicorn web process and a `release` command running `python manage.py migrate` on every deploy
- **GitHub** — version control and remote repository hosting. Every feature is committed incrementally with descriptive commit messages

### Development Tools

- **Git** — version control system used throughout development with granular, feature-level commits
- **VS Code** — primary code editor
- **Faker** — Python library used in the `seed_documents` management command to generate realistic fake document titles, descriptions and preview text for the seed data
- **ReportLab** — Python library used in the seed management command to generate dummy PDF files for seeded documents

### Validation Tools

- **W3C HTML Validator** — used to validate all HTML templates
- **W3C CSS Validator (Jigsaw)** — used to validate `static/css/style.css`
- **JSHint** — used to validate `checkout.js`
- **CI Python Linter (PEP8)** — used to validate all Python files against PEP8 style guidelines

### Django Packages

| Package                     | Version | Purpose                                          |
| --------------------------- | ------- | ------------------------------------------------ |
| `django`                    | 5.2     | Core framework                                   |
| `gunicorn`                  | 26.0.0  | Production WSGI server                           |
| `psycopg2-binary`           | 2.9.12  | PostgreSQL adapter                               |
| `dj-database-url`           | 3.1.2   | Parse DATABASE_URL into Django DATABASES         |
| `whitenoise`                | 6.12.0  | Static file serving in production                |
| `cloudinary`                | 1.44.2  | Cloudinary Python SDK                            |
| `django-cloudinary-storage` | 0.3.0   | Django storage backend for Cloudinary media      |
| `stripe`                    | 15.2.1  | Stripe Python SDK for payment processing         |
| `django-crispy-forms`       | 2.6     | Form rendering helpers                           |
| `crispy-bootstrap5`         | 2026.3  | Bootstrap 5 template pack for crispy forms       |
| `Faker`                     | 40.23.0 | Fake data generation for seed command            |
| `reportlab`                 | 5.0.0   | PDF generation for seed command                  |
| `pillow`                    | 12.2.0  | Image processing (required by Django ImageField) |

---

## Security Features

### Environment Variables and Secret Key Management

All sensitive credentials — including the Django `SECRET_KEY`, database connection string (`DATABASE_URL`), Stripe publishable and secret keys, Stripe webhook secret, and Cloudinary API credentials — are stored as environment variables and never committed to the repository. Locally these are loaded from `env.py`, which is listed in `.gitignore`. In production, all variables are set directly in Heroku's config vars via the CLI (`heroku config:set`). This ensures that no credentials are exposed in the codebase, git history or GitHub repository at any point.

### DEBUG Mode

`DEBUG` is controlled by an environment variable:

```python
DEBUG = os.environ.get("DEBUG", "False") == "True"
```

In local development `DEBUG=True` is set in `env.py`. On Heroku, the `DEBUG` config var is not set, so it defaults to `"False"`, meaning the production site never exposes stack traces, SQL queries or internal settings to end users. The custom `404.html` template is served instead of Django's debug error page when `DEBUG=False`.

### Authentication and Authorisation

- All views that require a logged-in user are decorated with `@login_required`, which redirects unauthenticated users to `/accounts/login/` automatically
- The login and register pages are only accessible to anonymous users — authenticated users are redirected to the homepage immediately
- Sellers can only edit or delete their own documents. The `edit_document` and `delete_document` views use `get_object_or_404(Document, slug=slug, seller=request.user)` — if a user attempts to access another seller's edit or delete URL, Django returns a 404 rather than an unauthorised error, preventing information disclosure
- Only buyers who have a `Purchase` record for a document can leave a review. The `add_review` view checks for a matching purchase before rendering the form or processing a submission
- Only buyers who have left a review can edit or delete it. The `edit_review` and `delete_review` views use `get_object_or_404(Review, id=review_id, reviewer=request.user)`

### Content Gating

The core security requirement of the project — that no regular user can access the full value of a document without paying — is enforced at two levels:

1. **View level:** The `document_detail` view queries the `Purchase` model before passing `has_purchased` to the template. The template renders the locked content card for unpurchased users and the unlocked card with a download link only for users with a confirmed purchase record.

2. **Webhook level:** The Stripe webhook view (`stripe_webhook`) listens for `payment_intent.succeeded` events sent directly from Stripe's servers. It verifies the event signature using `stripe.Webhook.construct_event` and the `STRIPE_WEBHOOK_SECRET` before creating a `Purchase` record. This ensures that even if a buyer closes their browser before reaching the success page, the purchase is still recorded and access is granted.

### CSRF Protection

Django's `CsrfViewMiddleware` is active in the middleware stack, providing CSRF protection on all POST requests including the login form, logout form, checkout, review submission, document upload and all delete confirmations. The Stripe webhook view is the only exception — it is decorated with `@csrf_exempt` because Stripe's servers cannot provide a Django CSRF token, and the request is instead verified using Stripe's own signature verification mechanism.

### Password Security

Django's default password hashing framework is used, which applies PBKDF2 with a SHA256 hash and a random salt by default. Passwords are never stored in plain text. Django's built-in `AUTH_PASSWORD_VALIDATORS` are configured to enforce minimum length, reject common passwords, reject purely numeric passwords, and reject passwords too similar to the username.

### Database Access

No raw SQL is used anywhere in the codebase. All database interactions go through Django's ORM, which parameterises all queries automatically and provides protection against SQL injection. Regular users have no direct access to the database — all reads and writes must pass through the application's views and model layer.

### Sensitive Data in Logs

Django's `SafeExceptionReporterFilter` is active by default, which redacts sensitive settings values (such as `SECRET_KEY`, `DATABASE_URL` and Stripe keys) from error reports and the Heroku log output, even when an uncaught exception occurs.

---

## Deployment

### Prerequisites

Before deploying, ensure you have the following installed and configured:

- Python 3.12
- Git
- Heroku CLI (`brew install heroku` on macOS)
- A [Heroku](https://heroku.com) account
- A [Neon](https://neon.tech) PostgreSQL database
- A [Cloudinary](https://cloudinary.com) account
- A [Stripe](https://stripe.com) account with test mode enabled

---

### Clone the Repository

```bash
git clone https://github.com/fahim2023/study-market.git
cd study-market
```

---

### Local Development Setup

1. **Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Create `env.py` in the project root**

```python
import os

os.environ.setdefault("SECRET_KEY", "your-secret-key-here")
os.environ.setdefault("DEBUG", "True")
os.environ.setdefault("DATABASE_URL", "your-neon-postgres-url-here")
os.environ.setdefault("STRIPE_PUBLIC_KEY", "pk_test_your-key-here")
os.environ.setdefault("STRIPE_SECRET_KEY", "sk_test_your-key-here")
os.environ.setdefault("STRIPE_WEBHOOK_SECRET", "whsec_your-key-here")
os.environ.setdefault("CLOUDINARY_CLOUD_NAME", "your-cloud-name")
os.environ.setdefault("CLOUDINARY_API_KEY", "your-api-key")
os.environ.setdefault("CLOUDINARY_API_SECRET", "your-api-secret")
```

> `env.py` is listed in `.gitignore` and must never be committed to the repository.

4. **Apply migrations**

```bash
python manage.py migrate
```

5. **Create a superuser**

```bash
python manage.py createsuperuser
```

6. **Seed the database with sample documents (optional)**

```bash
python manage.py seed_documents
```

7. **Run the development server**

```bash
python manage.py runserver
```

The site will be available at `http://127.0.0.1:8000/`.

---

### Deploy to Heroku

1. **Log in to Heroku**

```bash
heroku login
```

2. **Create a new Heroku app**

```bash
heroku create your-app-name
```

3. **Set all environment variables in Heroku config vars**

```bash
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set DEBUG=False
heroku config:set DATABASE_URL=your-neon-postgres-url-here
heroku config:set STRIPE_PUBLIC_KEY=pk_test_your-key-here
heroku config:set STRIPE_SECRET_KEY=sk_test_your-key-here
heroku config:set STRIPE_WEBHOOK_SECRET=whsec_your-key-here
heroku config:set CLOUDINARY_CLOUD_NAME=your-cloud-name
heroku config:set CLOUDINARY_API_KEY=your-api-key
heroku config:set CLOUDINARY_API_SECRET=your-api-secret
heroku config:set DISABLE_COLLECTSTATIC=1
```

> `DISABLE_COLLECTSTATIC=1` is required because `django-cloudinary-storage` is incompatible with Django 5.2's `collectstatic` command (see Bug 16). Static files are collected locally and committed to the repository instead.

4. **Confirm the `Procfile` exists in the project root**

```
web: gunicorn studymarket.wsgi:application --log-file -
release: python manage.py migrate
```

The `release` command runs `migrate` automatically on every deploy before traffic is switched to the new release.

5. **Collect static files locally and commit**

Before pushing to Heroku, temporarily comment out `cloudinary_storage` and `cloudinary` from `INSTALLED_APPS` in `settings.py`, run collectstatic, then uncomment:

```bash
python manage.py collectstatic --noinput
git add staticfiles/
git commit -m "Update staticfiles manifest"
```

6. **Push to Heroku**

```bash
git push heroku main
```

7. **Verify the deployment**

```bash
heroku open
heroku logs --tail
```

---

### Stripe Webhook Setup

1. Log in to the [Stripe Dashboard](https://dashboard.stripe.com)
2. Go to **Developers → Webhooks → Add destination**
3. Set the endpoint URL to `https://your-app-name.herokuapp.com/payments/webhook/`
4. Select the event `payment_intent.succeeded`
5. Copy the signing secret (`whsec_...`) and set it as a Heroku config var:

```bash
heroku config:set STRIPE_WEBHOOK_SECRET=whsec_your-signing-secret
```

---

### Static and Media Files

**Static files** (CSS, JS, images) are served by Whitenoise directly from Django in production. They are collected locally using `python manage.py collectstatic` and the resulting `staticfiles/` directory is committed to the repository. Heroku's automatic `collectstatic` step is disabled via `DISABLE_COLLECTSTATIC=1` due to the `django-cloudinary-storage` incompatibility with Django 5.2 (see Bug 16).

**Media files** (user-uploaded PDFs) are stored on Cloudinary using the `cloudinary_storage.storage.MediaCloudinaryStorage` backend. Cloudinary provides persistent storage that survives Heroku dyno restarts, which would otherwise wipe any files uploaded to Heroku's ephemeral filesystem. The Cloudinary free plan supports files up to 10MB — file size validation is enforced at form level in `DocumentForm.clean_file()` to prevent uploads exceeding this limit.

---

### Environment Variables Reference

| Variable                | Description                                 | Where to obtain                                                                                                            |
| ----------------------- | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `SECRET_KEY`            | Django secret key                           | Generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG`                 | Django debug mode                           | Set to `False` in production                                                                                               |
| `DATABASE_URL`          | PostgreSQL connection string                | Neon dashboard → Connection string                                                                                         |
| `STRIPE_PUBLIC_KEY`     | Stripe publishable key (`pk_test_...`)      | Stripe dashboard → Developers → API keys                                                                                   |
| `STRIPE_SECRET_KEY`     | Stripe secret key (`sk_test_...`)           | Stripe dashboard → Developers → API keys                                                                                   |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret (`whsec_...`) | Stripe dashboard → Developers → Webhooks                                                                                   |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name                       | Cloudinary dashboard → API Keys                                                                                            |
| `CLOUDINARY_API_KEY`    | Cloudinary API key                          | Cloudinary dashboard → API Keys                                                                                            |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret                       | Cloudinary dashboard → API Keys                                                                                            |
| `DISABLE_COLLECTSTATIC` | Disables Heroku's automatic collectstatic   | Set to `1`                                                                                                                 |

---

## Testing

### Automated Testing

All automated tests use Django's built-in testing framework. Tests run against a local SQLite database rather than the production Neon Postgres instance — hosted Postgres connection pooling conflicts with Django's test runner repeatedly creating/destroying a throwaway test database, so `settings.py` routes test runs to SQLite explicitly (see Bug 4).

#### accounts app

| Test                                                  | Description                                                                    | Result | Screenshot                                                                  |
| ----------------------------------------------------- | ------------------------------------------------------------------------------ | ------ | --------------------------------------------------------------------------- |
| `test_profile_created_automatically_on_user_creation` | A Profile is created automatically via signal when a new User registers        | Pass   | ![](documentation/images/testing/test-accounts-profile-created-pass.png)    |
| `test_new_profile_defaults_to_not_a_seller`           | A newly created Profile defaults `is_seller` to False                          | Pass   | ![](documentation/images/testing/test-accounts-default-not-seller-pass.png) |
| `test_subject_slug_auto_generated`                    | Subject slug is auto-generated from the subject name on save                   | Pass   | ![](documentation/images/testing/test-courses-subject-slug-pass.png)        |
| `test_course_slug_auto_generated`                     | Course slug is auto-generated from subject name, course name and level on save | Pass   | ![](documentation/images/testing/test-courses-course-slug-pass.png)         |
| `test_tag_str_returns_name`                           | DocumentTag string representation returns the tag name                         | Pass   | ![](documentation/images/testing/test-documents-tag-str-pass.png)           |
| `test_document_slug_auto_generated`                   | Document slug is auto-generated from the title on save                         | Pass   | ![](documentation/images/testing/test-documents-slug-pass.png)              |

#### payments app

| Test                                | Description                                                                                                                       | Result  | Screenshot                                             |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------ |
| `test_purchase_str`                 | Purchase `__str__` returns correct format `buyer → document title`                                                                | ✅ Pass | ![](documentation/images/testing/payments-test-01.png) |
| `test_duplicate_purchase_prevented` | Attempting to create a duplicate Purchase for the same buyer and document raises an exception due to `unique_together` constraint | ✅ Pass | ![](documentation/images/testing/payments-test-02.png) |
| `test_checkout_requires_login`      | Unauthenticated users attempting to access the checkout page are redirected to the login page with a 302 response                 | ✅ Pass | ![](documentation/images/testing/payments-test-03.png) |

#### reviews app

| Test                                  | Description                                                                                              | Result  | Screenshot                                            |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------- | ------- | ----------------------------------------------------- |
| `test_review_str`                     | Review `__str__` returns correct format `reviewer — document title (rating★)`                            | ✅ Pass | ![](documentation/images/testing/reviews-test-01.png) |
| `test_unpurchased_user_cannot_review` | A user who has not purchased a document is redirected away from the review form and no review is created | ✅ Pass | ![](documentation/images/testing/reviews-test-02.png) |
| `test_purchased_user_can_review`      | A user who has purchased a document can successfully submit a review which is saved to the database      | ✅ Pass | ![](documentation/images/testing/reviews-test-03.png) |

---

### Manual Testing

All manual tests were carried out on the live Heroku deployment at `https://study-market-fahim-70194c90b021.herokuapp.com/`.

| #   | User Story                                                                 | Test                                                                                                                                         | Expected Result                                                                                                       | Actual Result                                                 | Pass/Fail | Screenshot                                                                |
| --- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- | --------- | ------------------------------------------------------------------------- |
| 1   | As a visitor I can browse all published documents without registering      | Navigate to `/documents/browse/` while logged out                                                                                            | Browse page loads showing all published documents with no login required                                              | Browse page loaded correctly showing all documents            | ✅ Pass   | ![](documentation/images/testing/manual/manual-01-browse-logged-out.png)  |
| 2   | As a visitor I can view a document's title, course, price and preview text | Navigate to any document detail page while logged out                                                                                        | Document title, course badge, price, preview text and seller info are all visible                                     | All document details visible without login                    | ✅ Pass   | ![](documentation/images/testing/manual/manual-02-preview-logged-out.png) |
| 3   | As a visitor I cannot view full document content without paying            | Navigate to any document detail page while logged out                                                                                        | Locked content card shown with lock icon and Unlock CTA, full content and download not accessible                     | Locked card rendered correctly with no access to full content | ✅ Pass   | ![](documentation/images/testing/manual/manual-03-locked-content.png)     |
| 4   | As a visitor I can register an account                                     | Navigate to `/accounts/register/`, fill in form and submit                                                                                   | Account is created and user is redirected to homepage with success message                                            | Account created successfully, redirected to homepage          | ✅ Pass   | ![](documentation/images/testing/manual/manual-04-register-success.png)   |
| 5   | As a visitor I can log in                                                  | Navigate to `/accounts/login/`, enter credentials and submit                                                                                 | User is logged in and redirected to homepage with welcome message                                                     | Logged in successfully, redirected to homepage                | ✅ Pass   | ![](documentation/images/testing/manual/manual-05-login-success.png)      |
| 6   | As a buyer I can search documents by keyword                               | Enter a keyword in the search bar and submit                                                                                                 | Browse page filters to show only documents matching the keyword                                                       | Documents filtered correctly by keyword                       | ✅ Pass   | ![](documentation/images/testing/manual/manual-06-search.png)             |
| 7   | As a buyer I can filter documents by subject                               | Select a subject radio button in the sidebar and click Apply Filters                                                                         | Browse page filters to show only documents in the selected subject                                                    | Documents filtered correctly by subject                       | ✅ Pass   | ![](documentation/images/testing/manual/manual-07-filter-subject.png)     |
| 8   | As a buyer I can purchase a document via Stripe                            | Navigate to checkout, enter test card `4242 4242 4242 4242`, expiry `12/34`, CVC `123` and click Pay                                         | Payment is processed, Purchase record created, redirected to success page                                             | Payment processed successfully, redirected to success page    | ✅ Pass   | ![](documentation/images/testing/manual/manual-08-checkout-card.png)      |
| 9   | As a buyer I receive clear confirmation after payment                      | Complete a Stripe test payment                                                                                                               | Payment success page rendered with confirmation message                                                               | Success page rendered correctly                               | ✅ Pass   | ![](documentation/images/testing/manual/manual-09-payment-success.png)    |
| 10  | As a buyer I can view and download purchased documents from My Purchases   | Navigate to `/payments/my-purchases/` after purchasing a document                                                                            | My Purchases page shows purchased documents with View Now and PDF download buttons                                    | All purchased documents listed with correct buttons           | ✅ Pass   | ![](documentation/images/testing/manual/manual-10-my-purchases.png)       |
| 11  | As a buyer I can leave a review on a purchased document                    | Navigate to `/reviews/add/<id>/` for a purchased document, fill in form and submit                                                           | Review is saved and shown on the document detail page                                                                 | Review submitted and displayed correctly                      | ✅ Pass   | ![](documentation/images/testing/manual/manual-11-review-submitted.png)   |
| 12  | As a buyer I cannot review a document I have not purchased                 | Navigate to `/reviews/add/<id>/` for an unpurchased document                                                                                 | User is redirected to document detail page with error alert "You must purchase this document before leaving a review" | Redirected correctly with styled error alert                  | ✅ Pass   | ![](documentation/images/testing/manual/manual-12-review-blocked.png)     |
| 13  | As a buyer I can edit my review                                            | Navigate to `/reviews/edit/<id>/`, change the review and submit                                                                              | Review is updated and changes are reflected on the document detail page                                               | Review updated successfully                                   | ✅ Pass   | ![](documentation/images/testing/manual/manual-13-edit-review.png)        |
| 14  | As a buyer I can delete my review                                          | Navigate to `/reviews/delete/<id>/`, confirm deletion                                                                                        | Review is deleted and no longer appears on the document detail page                                                   | Review deleted successfully                                   | ✅ Pass   | ![](documentation/images/testing/manual/manual-14-delete-review.png)      |
| 15  | As a seller I can upload a new document                                    | Navigate to `/documents/seller/upload/`, fill in form, upload a PDF and submit                                                               | Document is created and appears in the seller dashboard                                                               | Document uploaded and visible in dashboard                    | ✅ Pass   | ![](documentation/images/testing/manual/manual-15-upload-success.png)     |
| 16  | As a seller I can see all my listings on a dashboard                       | Navigate to `/documents/seller/dashboard/`                                                                                                   | Seller dashboard shows all uploaded documents with title, subject, price, status and action buttons                   | All documents listed correctly                                | ✅ Pass   | ![](documentation/images/testing/manual/manual-16-dashboard.png)          |
| 17  | As a seller I can edit my own listings                                     | Click the edit icon on a listing in the dashboard, change a field and submit                                                                 | Document is updated and changes are reflected in the dashboard and detail page                                        | Document updated successfully                                 | ✅ Pass   | ![](documentation/images/testing/manual/manual-17-edit-document.png)      |
| 18  | As a seller I can delete my own listings                                   | Click the delete icon on a listing in the dashboard and confirm                                                                              | Document is deleted and no longer appears in the dashboard or browse page                                             | Document deleted successfully                                 | ✅ Pass   | ![](documentation/images/testing/manual/manual-18-delete-document.png)    |
| 19  | As a seller I cannot edit or delete another seller's listings              | While logged in as `fahim`, navigate to `/documents/seller/edit/market-structures-past-paper-solutions/` which belongs to a different seller | Custom 404 page returned — document not found for this seller                                                         | 404 page returned correctly, no access granted                | ✅ Pass   | ![](documentation/images/testing/manual/manual-19-edit-blocked-404.png)   |
| 20  | As an admin I can manage subjects and courses                              | Navigate to `/admin/courses/subject/` while logged in as superuser                                                                           | Subject list visible with add/edit/delete functionality                                                               | Subjects manageable via admin panel                           | ✅ Pass   | ![](documentation/images/testing/manual/manual-20-admin-subjects.png)     |
| 21  | As an admin I can view all purchases                                       | Navigate to `/admin/payments/purchase/` while logged in as superuser                                                                         | All purchase records visible with buyer, document, amount and date                                                    | All purchases listed correctly in admin                       | ✅ Pass   | ![](documentation/images/testing/manual/manual-21-admin-purchases.png)    |
| 22  | As an admin I can moderate reviews                                         | Navigate to `/admin/reviews/review/` while logged in as superuser                                                                            | All reviews visible with edit and delete functionality                                                                | Reviews manageable via admin panel                            | ✅ Pass   | ![](documentation/images/testing/manual/manual-22-admin-reviews.png)      |

_(User story → test → expected → actual → pass/fail table — to be completed.)_

---

### Validator Testing

#### HTML Validation

All pages were validated using the [W3C Nu HTML Checker](https://validator.w3.org/nu/). Public pages were validated via direct URL. Pages requiring authentication were validated by copying the page source and pasting into the text input validator.

One issue was identified and fixed during validation: the Add Review page had a heading hierarchy starting at `<h2>` with no preceding `<h1>`. This was corrected by changing the heading to `<h1>` with Bootstrap's `h2` class applied to maintain visual size. The footer column headings were also changed from `<h3>` to `<h2>` to avoid skipping heading levels after the page `<h1>`.

| Page             | Method      | Result    | Screenshot                                                                  |
| ---------------- | ----------- | --------- | --------------------------------------------------------------------------- |
| Homepage         | Direct URL  | No errors | ![](documentation/images/testing/validation/html/html-homepage.png)         |
| Browse           | Direct URL  | No errors | ![](documentation/images/testing/validation/html/html-browse.png)           |
| Document Detail  | Direct URL  | No errors | ![](documentation/images/testing/validation/html/html-document-detail.png)  |
| Login            | Direct URL  | No errors | ![](documentation/images/testing/validation/html/html-login.png)            |
| Register         | Direct URL  | No errors | ![](documentation/images/testing/validation/html/html-register.png)         |
| 404 Page         | Page source | No errors | ![](documentation/images/testing/validation/html/html-404.png)              |
| My Purchases     | Page source | No errors | ![](documentation/images/testing/validation/html/html-my-purchases.png)     |
| Seller Dashboard | Page source | No errors | ![](documentation/images/testing/validation/html/html-seller-dashboard.png) |
| Upload Document  | Page source | No errors | ![](documentation/images/testing/validation/html/html-upload.png)           |
| Checkout         | Page source | No errors | ![](documentation/images/testing/validation/html/html-checkout.png)         |
| Add Review       | Page source | No errors | ![](documentation/images/testing/validation/html/html-add-review.png)       |

#### CSS Validation

The CSS file `static/css/style.css` was validated using the [W3C CSS Validator (Jigsaw)](https://jigsaw.w3.org/css-validator/) via direct input. No errors were found.

18 warnings were returned, all of which are expected and acceptable:

- **CSS variables not statically checked** — the validator cannot evaluate `var()` custom properties at validation time. This is a known limitation of the validator and not an indication of any issue with the code.
- **Same colour for `background-color` and `border-color`** — intentional in the button design system where border and background match to create solid filled buttons.

![CSS Validation](documentation/images/testing/validation/css/css-validation.png)

#### Python PEP8 Validation

All Python files were validated using the [CI Python Linter](https://pep8ci.herokuapp.com/). `autopep8` was run across the project with `--max-line-length 79 --recursive` to automatically fix line length issues. Remaining long lines in `AUTH_PASSWORD_VALIDATORS` in `settings.py` were fixed by splitting the validator class paths across multiple lines using Python string concatenation.

| File                      | Result    | Screenshot                                                                    |
| ------------------------- | --------- | ----------------------------------------------------------------------------- |
| `studymarket/settings.py` | No errors | ![](documentation/images/testing/validation/python/pep8-settings.png)         |
| `studymarket/urls.py`     | No errors | ![](documentation/images/testing/validation/python/pep8-studymarket-urls.png) |
| `accounts/admin.py`       | No errors | ![](documentation/images/testing/validation/python/pep8-accounts-admin.png)   |
| `accounts/apps.py`        | No errors | ![](documentation/images/testing/validation/python/pep8-accounts-apps.png)    |
| `accounts/forms.py`       | No errors | ![](documentation/images/testing/validation/python/pep8-accounts-forms.png)   |
| `accounts/models.py`      | No errors | ![](documentation/images/testing/validation/python/pep8-accounts-models.png)  |
| `accounts/signals.py`     | No errors | ![](documentation/images/testing/validation/python/pep8-accounts-signals.png) |
| `accounts/urls.py`        | No errors | ![](documentation/images/testing/validation/python/pep8-accounts-urls.png)    |
| `accounts/views.py`       | No errors | ![](documentation/images/testing/validation/python/pep8-accounts-views.png)   |
| `courses/admin.py`        | No errors | ![](documentation/images/testing/validation/python/pep8-courses-admin.png)    |
| `courses/apps.py`         | No errors | ![](documentation/images/testing/validation/python/pep8-courses-apps.png)     |
| `courses/models.py`       | No errors | ![](documentation/images/testing/validation/python/pep8-courses-models.png)   |
| `courses/urls.py`         | No errors | ![](documentation/images/testing/validation/python/pep8-courses-urls.png)     |
| `documents/admin.py`      | No errors | ![](documentation/images/testing/validation/python/pep8-document-admin.png)   |
| `documents/apps.py`       | No errors | ![](documentation/images/testing/validation/python/pep8-documents-apps.png)   |
| `documents/forms.py`      | No errors | ![](documentation/images/testing/validation/python/pep8-documents-forms.png)  |
| `documents/models.py`     | No errors | ![](documentation/images/testing/validation/python/pep8-documents-models.png) |
| `documents/urls.py`       | No errors | ![](documentation/images/testing/validation/python/pep8-documents-urls.png)   |
| `documents/views.py`      | No errors | ![](documentation/images/testing/validation/python/pep8-document-views.png)   |
| `home/apps.py`            | No errors | ![](documentation/images/testing/validation/python/pep8-home-apps.png)        |
| `home/urls.py`            | No errors | ![](documentation/images/testing/validation/python/pep8-home-urls.png)        |
| `home/views.py`           | No errors | ![](documentation/images/testing/validation/python/pep8-home-views.png)       |
| `payments/admin.py`       | No errors | ![](documentation/images/testing/validation/python/pep8-payments-admin.png)   |
| `payments/apps.py`        | No errors | ![](documentation/images/testing/validation/python/pep8-payments-apps.png)    |
| `payments/models.py`      | No errors | ![](documentation/images/testing/validation/python/pep8-payments-models.png)  |
| `payments/urls.py`        | No errors | ![](documentation/images/testing/validation/python/pep8-payments-urls.png)    |
| `payments/views.py`       | No errors | ![](documentation/images/testing/validation/python/pep8-payments-views.png)   |
| `reviews/admin.py`        | No errors | ![](documentation/images/testing/validation/python/pep8-reviews-admin.png)    |
| `reviews/apps.py`         | No errors | ![](documentation/images/testing/validation/python/pep8-reviews-apps.png)     |
| `reviews/forms.py`        | No errors | ![](documentation/images/testing/validation/python/pep8-reviews-forms.png)    |
| `reviews/models.py`       | No errors | ![](documentation/images/testing/validation/python/pep8-reviews-models.png)   |
| `reviews/urls.py`         | No errors | ![](documentation/images/testing/validation/python/pep8-reviews-urls.png)     |
| `reviews/views.py`        | No errors | ![](documentation/images/testing/validation/python/pep8-reviews-views.png)    |

#### JavaScript Validation

Both JavaScript files were validated using [JSHint](https://jshint.com/).

**`checkout.js`**

`/* jshint esversion: 8 */` and `/* global Stripe */` were added to the top of the file to inform JSHint that ES8 syntax is intentional and that `Stripe` is a global variable loaded from the Stripe.js CDN. After adding these directives, one warning remained:

- **`clientSecret` unused variable** — this variable is declared but used indirectly via `data.client_secret` from the POST response. It is not a real issue and does not affect functionality.

No errors were found.

![JS Checkout Validation](documentation/images/testing/validation/js/js-checkout.png)

**`alerts.js`**

No errors or warnings found.

![JS Alerts Validation](documentation/images/testing/validation/js/js-alerts.png)

#### Lighthouse

_(Lighthouse scores for key pages — to be completed.)_

---

### Responsiveness

_(Chrome / Safari / Firefox × Desktop / Tablet / Mobile — to be completed.)_

---

## Bugs

### Bug 1 — Heroku push rejected: no default language detected

- **Issue:** `git push heroku main` was rejected with "No default language could be detected for this app", even though `requirements.txt` existed in the repository.
- **Root cause:** Two compounding problems. First, no buildpack had been explicitly set on the Heroku app. Second — and the real culprit — the local git repository's root (`.git` folder) was sitting one level above the actual project folder (`~/Desktop` instead of `~/Desktop/study_market`), so every tracked file was nested under an extra `study_market/` prefix in the repo. Heroku was therefore looking for `requirements.txt` at the repo root and not finding it, since it was actually one directory deeper.
- **Fix:**
  1. Explicitly set the buildpack: `heroku buildpacks:set heroku/python`
  2. Moved the `.git` folder into the correct project directory so the repo root matches the project root: `mv ~/Desktop/.git ~/Desktop/study_market/.git`
  3. Restaged and committed the resulting path changes so all files (`manage.py`, `requirements.txt`, etc.) sit at the top level of the repository.

```bash
heroku buildpacks:set heroku/python
mv ~/Desktop/.git ~/Desktop/study_market/.git
cd ~/Desktop/study_market
git add -A
git commit -m "Fix repository root to match project structure"
git push origin main
git push heroku main
```

---

### Bug 2 — Invalid Python version in runtime.txt

- **Issue:** After fixing Bug 1, the build reached the Python detection step but failed with "Invalid Python version in runtime.txt".
- **Root cause:** `runtime.txt` is Heroku's older, now-deprecated method for pinning a Python version. Heroku's current buildpack expects a `.python-version` file instead, containing only the major version number (no `python-` prefix, no patch version).
- **Fix:** Removed `runtime.txt` and replaced it with `.python-version` containing just the major version.

**Before** ![screenshot](documentation/images/bugs/bug-01-heroku-buildpack.png)
**After** ![screenshot](documentation/images/bugs/bug-01-heroku-buildpack-after.png)

---

### Bug 3 — collectstatic failed: STATIC_ROOT not set

- **Issue:** After fixing Bugs 1 and 2, the Heroku build progressed further but then failed during the automatic `python manage.py collectstatic --noinput` step, raising `django.core.exceptions.ImproperlyConfigured: You're using the staticfiles app without having set the STATIC_ROOT setting to a filesystem path.`
- **Root cause:** `STATIC_ROOT` had never been added to `settings.py`. In development, Django's dev server serves static files automatically and doesn't need this setting, so the omission only surfaced once `DEBUG=False` and Heroku's build pipeline tried to gather all static files into a single deployable folder.
- **Fix:** Added `STATIC_ROOT` pointing at a `staticfiles` folder, and configured Whitenoise's compressed manifest storage backend so static files are served efficiently in production. Also confirmed `whitenoise.middleware.WhiteNoiseMiddleware` was present in `MIDDLEWARE`, directly after `SecurityMiddleware`.

**Before (`settings.py`):**

```python
STATIC_URL = 'static/'
```

**After (`settings.py`):**

```python
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

- **Screenshot:** ![Bug 3](documentation/images/bugs/bug-03-static-root.png)

---

### Bug 4 — Test database errors against hosted Postgres (Neon)

- **Issue:** Running `python manage.py test accounts` passed the actual test, but then crashed during teardown with `psycopg2.errors.ObjectInUse: database "test_neondb" is being accessed by other users`.
- **Root cause:** Django's test runner creates a throwaway test database and destroys it after the run. Neon's connection pooling keeps a session open against the database in a way that blocks Postgres from dropping it, so the teardown step fails and leaves a stale `test_neondb` behind.
- **Fix:** Routed test runs to a local SQLite database instead of Neon.

**Added to `settings.py`:**

```python
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }
```

---

### Bug 5 — Heroku release command failed: missing login_view function

- **Issue:** `git push heroku main` built and deployed successfully, but the automatic `release: python manage.py migrate` step then failed with `AttributeError: module 'accounts.views' has no attribute 'login_view'`.
- **Root cause:** `accounts/urls.py` referenced `views.login_view`, but a custom `login_view` function had not yet been written in `accounts/views.py` at the time of that commit.
- **Fix:** Added the missing `login_view` function to `accounts/views.py`.

- **Screenshot:** ![Bug 5](documentation/images/bugs/bug-05-login-view-error.png)

---

### Bug 6 — Custom CSS not applying: missing STATICFILES_DIRS

- **Issue:** The site rendered with default Bootstrap colours instead of the custom teal/amber design system palette, even though `style.css` had the right content.
- **Root cause:** `STATICFILES_DIRS` was missing from `settings.py`. Without it, Django had no way to locate `style.css` at all during development.
- **Fix:** Added `STATICFILES_DIRS = [BASE_DIR / "static"]` to `settings.py`.

**Before:** ![Bug 6 before](documentation/images/bugs/bug-06-static-before.png)
**After:** ![Bug 6 after](documentation/images/bugs/bug-06-static-after.png)

---

### Bug 7 — InvalidStorageError: missing 'default' key in STORAGES

- **Issue:** Attempting to save a `Document` with a file upload crashed with `django.core.files.storage.handler.InvalidStorageError: Could not find config for 'default' in settings.STORAGES`.
- **Root cause:** The `STORAGES` setting only defined the `staticfiles` backend. Django's `FileField` also requires a `default` backend for media file uploads.
- **Fix:** Added the `default` key to `STORAGES`.

**Before:** ![Bug 7 before](documentation/images/bugs/bug-07-storage-before.png)
**After:** ![Bug 7 after](documentation/images/bugs/bug-07-storage-after.png)

---

### Bug 8: `{% load static %}` placed before `{% extends %}` in checkout template

**Issue:** `TemplateSyntaxError` at `/payments/checkout/242/` — `{% extends "base.html" %} must be the first tag in 'payments/checkout.html'`.

![Bug 8 before fix](documentation/images/bugs/bug-08-extends-before.png)

**Cause:** When separating the Stripe JavaScript into a static file, `{% load static %}` was added to line 1, pushing `{% extends "base.html" %}` to line 2. Django requires `{% extends %}` to be the absolute first tag in any template that inherits from a base.

**Fix:** Swapped the order so `{% extends "base.html" %}` appears on line 1 and `{% load static %}` on line 2.

![Bug 8 after fix](documentation/images/bugs/bug-08-extends-after.png)

---

### Bug 9: Footer not sticking to bottom of page on short pages

**Issue:** On pages with little content, the footer floated halfway up the screen leaving a large blank gap below it.

![Bug 9 before fix](documentation/images/bugs/bug-09-footer-before.png)

**Cause:** The `body` element had no minimum height set, so on short pages the footer rendered immediately after the content.

**Fix:** Added `min-height: 100vh` and `display: flex; flex-direction: column` to `body` in `style.css`, and `flex: 1` to `main`.

![Bug 9 after fix](documentation/images/bugs/bug-09-footer-after.png)

---

### Bug 10: Checkout page throwing UnboundLocalError and payment not completing

Three related issues prevented the payment flow from working end to end.

**Issue 1 — UnboundLocalError on GET request**

![Bug 10 before - UnboundLocalError](documentation/images/bugs/bug-10-unbound-intent-before.png)

**Cause:** The `return JsonResponse` statement was outside the `if request.method == "POST"` block. On a GET request, `intent` is never created so Python raised an error accessing `intent.client_secret`.

**Fix:** Moved `return JsonResponse` inside the POST block and added a `return render` for GET requests.

```python
# Fixed
if request.method == "POST":
    intent = stripe.PaymentIntent.create(...)
    return JsonResponse({"client_secret": intent.client_secret})

return render(request, "payments/checkout.html", {
    "document": document,
    "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
})
```

**Issue 2 — Postal code field blocking payment**

![Bug 10 before - postal code](documentation/images/bugs/bug-10-postal-code-before.png)

**Cause:** Stripe's card element defaults to US postal code format (5 numeric digits). UK postcodes contain letters so the field could never be completed.

**Fix:** Added `hidePostalCode: true` to the card element options in `checkout.js`.

```javascript
const card = elements.create("card", { hidePostalCode: true });
```

**Issue 3 — client_secret not being passed to Stripe**

![Bug 10 before - console error](documentation/images/bugs/bug-10-client-secret-console-before.png)

**Cause:** The JS was reading `clientSecret` from an HTML data attribute set at page load, which is empty on GET because no PaymentIntent exists until form submission.

**Fix:** Changed the JS to use `data.client_secret` from the POST response.

```javascript
const data = await response.json();
const result = await stripe.confirmCardPayment(data.client_secret, {
  payment_method: { card: card },
});
```

![Bug 10 after - payment success](documentation/images/bugs/bug-10-payment-success-after.png)

---

### Bug 11: Incorrect field name `title` used in payments test setUp

**Cause:** `Course` model uses `name` not `title`. Caught by the test runner.

**Fix:** Changed `title='A-Level Maths'` to `name='A-Level Maths'` in `payments/tests.py`.

---

### Bug 12: Footer missing on deployed Heroku site

**Issue:** The footer was visible locally but completely absent on Heroku.

![Bug 12 before fix](documentation/images/bugs/bug-12-footer-missing-before.png)

**Cause:** The `{% include 'includes/footer.html' %}` line had been added to `base.html` locally but never committed to git. Confirmed with `git show HEAD:templates/base.html | grep footer` which returned nothing.

**Fix:** Staged and committed `templates/base.html` with the footer include in place.

![Bug 12 after fix](documentation/images/bugs/bug-12-footer-missing-after.png)

---

### Bug 13: Reviews section missing from document detail page

**Issue:** After deleting a review, the reviews section disappeared entirely — including the "Write a Review" button.

![Bug 13 before fix](documentation/images/bugs/bug-13-reviews-section-missing-before.png)

**Cause:** When the detail template was rewritten to wire up checkout buttons, the reviews section lost its wrapping card container and the `{% if has_purchased and not user_has_reviewed %}` block.

**Fix:** Rewrote the reviews section with the correct card wrapper, fallback "No reviews yet" message and conditional "Write a Review" button.

![Bug 13 after fix](documentation/images/bugs/bug-13-reviews-section-missing-after.png)

---

### Bug 14: Heroku 500 error on document detail page after reviews app added

**Issue:** All document detail pages threw 500 Internal Server Error on Heroku while working locally.

![Bug 14 before fix](documentation/images/bugs/bug-14-heroku-500-before.png)

**Cause:** Several local changes had never been staged and committed — most critically, `reviews` was added to `INSTALLED_APPS` locally but the updated `settings.py` was never committed, so Heroku threw `RuntimeError: Model class reviews.models.Review doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS`.

**Fix:** Ran `git status`, identified all uncommitted files, staged and committed everything.

**Prevention:** Always run `git status` before pushing. Each feature should be committed in its entirety before moving on.

![Bug 14 after fix](documentation/images/bugs/bug-14-heroku-500-after.png)

---

### Bug 15: Stripe publishable key not set on Heroku causing payments to fail

**Issue:** On the live site, clicking Unlock did nothing. The browser console showed `Uncaught IntegrationError: Please call Stripe() with your publishable key. You used an empty string.`

![Bug 15 before fix](documentation/images/bugs/bug-15-stripe-public-key-before.png)

**Cause:** `STRIPE_PUBLIC_KEY` had not been set in Heroku's config vars. `env.py` is in `.gitignore` and never deployed — every variable in `env.py` must also be set manually in Heroku config vars. During the fix, the secret key (`sk_test_...`) was accidentally entered as the public key — this was caught immediately and corrected.

**Fix:**

```bash
heroku config:set STRIPE_PUBLIC_KEY=pk_test_...
heroku config:get STRIPE_PUBLIC_KEY
```

![Bug 15 after fix](documentation/images/bugs/bug-15-stripe-public-key-after.png)

---

### Bug 16: Cloudinary `django-cloudinary-storage` incompatible with Django 5.2 causing Heroku build failure

**Issue:** Every Heroku deploy failed during `collectstatic` with `AttributeError: 'Settings' object has no attribute 'STATICFILES_STORAGE'`.

![Bug 16 before fix](documentation/images/bugs/bug-16-cloudinary-collectstatic-before.png)

**Cause:** `django-cloudinary-storage==0.3.0` still references `settings.STATICFILES_STORAGE` which was removed in Django 5.2. The package itself needed updating but the maintainers had not released a compatible version.

**Fix:** Since Whitenoise handles static files, `collectstatic` was disabled on Heroku via:

```bash
heroku config:set DISABLE_COLLECTSTATIC=1
```

Static files are instead collected locally and committed to the repository.

![Bug 16 after fix](documentation/images/bugs/bug-16-cloudinary-collectstatic-after.png)

---

### Bug 17: NoReverseMatch on seller dashboard — edit and delete URLs not yet registered

**Issue:** After uploading a document, the redirect to the seller dashboard threw `NoReverseMatch: Reverse for 'edit' not found`.

![Bug 17 before fix](documentation/images/bugs/bug-17-no-reverse-match-before.png)

**Cause:** The `seller_dashboard.html` template was written with Edit and Delete buttons before the corresponding views and URL patterns had been built. Django resolves all `{% url %}` tags at render time and raises `NoReverseMatch` immediately if any named URL cannot be found.

**Fix:** Temporarily removed the Edit and Delete buttons from the dashboard template until the views and URLs were built.

---

### Bug 18: Upload page returning 404 at incorrect URL path

**Issue:** Navigating to `http://127.0.0.1:8000/seller/upload/` returned a 404 error.

![Bug 18 before fix](documentation/images/bugs/bug-18-upload-404-before.png)

**Cause:** The upload view is registered inside `documents/urls.py` which is included under the `documents/` prefix. The correct path is `http://127.0.0.1:8000/documents/seller/upload/`.

**Fix:** Used the correct full URL path. All internal links use `{% url 'documents:upload' %}` which Django resolves correctly.

---

### Bug 19: Cloudinary rejecting file uploads over 10MB with unhandled BadRequest exception

**Issue:** Uploading a 57MB PDF threw an unhandled `BadRequest: File size too large. Got 59705814. Maximum is 10485760.`

![Bug 19 before fix](documentation/images/bugs/bug-19-cloudinary-file-size-before.png)

**Cause:** `DocumentForm` had no file size validation — it accepted any file and only hit the Cloudinary limit after the full upload was sent to the API.

**Fix:** Added a `clean_file` method to `DocumentForm` to reject files over 10MB before any Cloudinary API call is made:

```python
def clean_file(self):
    file = self.cleaned_data.get('file')
    if file and file.size > 10 * 1024 * 1024:
        raise forms.ValidationError(
            'File size must be under 10MB. Please compress your PDF and try again.'
        )
    return file
```

---

### Bug 20: Login redirecting to browse page instead of homepage

**Issue:** After logging in, users were redirected to `/documents/browse/` instead of the homepage.

![Bug 20 before fix](documentation/images/bugs/bug-20-login-redirect-before.png)

**Cause:** The custom `login_view` had hardcoded `redirect("documents:browse")` which overrode the `LOGIN_REDIRECT_URL = 'home:home'` setting entirely. Django's `LOGIN_REDIRECT_URL` only applies to the built-in auth views, not custom views.

**Fix:** Updated both redirect calls in `accounts/views.py` to `redirect("home:home")`.

![Bug 20 after fix](documentation/images/bugs/bug-20-login-redirect-after.png)

---

### Bug 21: Heroku 500 error — missing staticfiles manifest entry for 'css/style.css'

**Issue:** After deploying, every page on Heroku threw 500 with `ValueError: Missing staticfiles manifest entry for 'css/style.css'`.

![Bug 21 before fix](documentation/images/bugs/bug-21-staticfiles-manifest-before.png)

**Cause:** Whitenoise's `CompressedManifestStaticFilesStorage` requires a `staticfiles.json` manifest generated by `collectstatic`. Since `DISABLE_COLLECTSTATIC=1` was set (Bug 16), Heroku never ran collectstatic. Additionally `staticfiles/` was in `.gitignore` so the locally-generated manifest was never committed. The Cloudinary incompatibility also prevented running collectstatic locally with Cloudinary installed.

**Fix:**

1. Temporarily commented out `cloudinary_storage` and `cloudinary` from `INSTALLED_APPS`
2. Ran `python manage.py collectstatic --noinput` locally
3. Removed `staticfiles/` from `.gitignore` and committed the manifest

```bash
git add staticfiles/ .gitignore
git commit -m "Add staticfiles manifest to repo to fix Heroku 500 error"
git push origin main
git push heroku main
```

![Bug 21 after fix](documentation/images/bugs/bug-21-staticfiles-manifest-after.png)

### Bug 22: Stripe secret key not set on Heroku causing checkout 500 error

**Issue:** On the live Heroku site, clicking Pay on the checkout page returned a 500 Internal Server Error. The browser console showed the POST to `/payments/checkout/` returning a 500 status with an HTML error page instead of the expected JSON `client_secret`, causing a `SyntaxError: Unexpected token '<'`. Checking `heroku logs --tail` confirmed the root cause:

```
stripe._error.AuthenticationError: You did not provide an API key. You need to provide your API key in the Authorization header, using Bearer auth (e.g. 'Authorization: Bearer YOUR_SECRET_KEY').
```

**Cause:** The `STRIPE_SECRET_KEY` environment variable had not been set in Heroku's config vars. Locally the key is loaded from `env.py`, but `env.py` is in `.gitignore` and is never deployed to Heroku. Without it, `stripe.api_key` was set to an empty string in `payments/views.py` at module load time:

```python
stripe.api_key = settings.STRIPE_SECRET_KEY
```

When the checkout view then attempted to call `stripe.PaymentIntent.create()`, Stripe's API rejected the request with a 401 authentication error, which Django surfaced as an unhandled 500 Internal Server Error. The JS received an HTML error page instead of the expected JSON containing the `client_secret`, causing the browser console `SyntaxError`.

This is the same class of issue as Bug 15 (missing `STRIPE_PUBLIC_KEY`) — every variable defined in `env.py` must also be set manually in Heroku's config vars. The public key controls client-side Stripe initialisation; the secret key controls server-side PaymentIntent creation. Both are required for the payment flow to work end to end on the live site.

**Fix:** Set the Stripe secret key in Heroku config vars:

```bash
heroku config:set STRIPE_SECRET_KEY=sk_test_...
```

After the dyno restarted with the correct key, the checkout view successfully created a PaymentIntent, returned the `client_secret` as JSON, and the full payment flow completed correctly on the live Heroku site.

## ![Bug 22 after fix](documentation/images/bugs/bug-22-stripe-secret-key-after.png)

### Bug 23: Edit document throwing 500 error when no new file uploaded

**Issue:** Editing a document on the live Heroku site threw a 500 Internal Server Error whenever the form was submitted without uploading a new file. The Heroku logs showed the error occurring in `documents/forms.py` at the `clean_file` method:

```
File "/app/documents/forms.py", line 40, in clean_file
if file and file.size > 10 * 1024 * 1024:
TypeError: '>' not supported between instances of 'NoneType' and 'int'
```

![Bug 23 before fix](documentation/images/bugs/bug-23-edit-document-before.png)

**Cause:** When editing a document without uploading a new file, Cloudinary returns a file object where `.size` is `None` rather than an integer. The `clean_file` validation method checked `if file and file.size > 10 * 1024 * 1024` — `file` was truthy (the Cloudinary object existed) but `file.size` was `None`, causing Python to throw a `TypeError` when comparing `None > int`. This only surfaced on Heroku because Cloudinary is only used in production — locally Django uses the filesystem storage backend where `.size` is always a valid integer.

**Fix:** Wrapped the size check in a `try/except` block to handle the case where `file.size` is `None` or raises an `AttributeError`:

```python
def clean_file(self):
    file = self.cleaned_data.get("file")
    try:
        if file and file.size and file.size > 10 * 1024 * 1024:
            raise forms.ValidationError(
                "File size must be under 10MB. Please compress your PDF and try again."
            )
    except (AttributeError, TypeError):
        pass
    return file
```

The `edit_document` view was also updated to preserve the existing file when no new file is uploaded:

```python
if not request.FILES.get('file'):
    doc.file = document.file
```

After deploying, editing a document without re-uploading the file worked correctly and redirected to the seller dashboard with a success message.

![Bug 23 after fix](documentation/images/bugs/bug-23-edit-document-after.png)

## Design Decisions

### Subject Management — Admin Only

The Subject model is intentionally restricted to admin management only. Sellers cannot create new subjects or courses through the site interface — they can only select from the existing taxonomy when uploading a document.

This was a deliberate architectural decision for the following reasons:

- **Data integrity:** Allowing users to freely create subjects would result in duplicates, misspellings and inconsistent categorisation (e.g. "Maths", "Mathematics", "Math" all appearing as separate subjects).
- **Taxonomy control:** The subject list represents the core organisational structure of the marketplace. Keeping it admin-controlled ensures it remains clean, consistent and meaningful for buyers browsing by subject.
- **Scope:** For the purposes of this project, the predefined subjects (Biology, Economics, History, Law, Mathematics, Psychology) cover the core academic domains. New subjects can be added by a site administrator via `/admin/` as the platform grows.

This is consistent with how real academic marketplaces manage their category taxonomies — categories are curated by the platform, not crowdsourced from sellers.

---

## Future Implementations

- Seller earnings dashboard showing total revenue and per-document sales counts
- Seller response to reviews
- Document tags for finer-grained filtering (e.g. "exam-style", "summary", "diagrams")
- Email notifications on purchase
- Subscription tier for buyers with unlimited access
- Verified seller badges based on review ratings

---

## Credits

### Content

All document titles, descriptions and preview text in the seed data were generated using the [Faker](https://faker.readthedocs.io/) Python library.

### Media

Subject thumbnail images and hero image were generated using [Google ImageFX](https://labs.google/fx/tools/image-fx) with custom prompts designed to match the StudyMarket teal/amber colour palette.

### Design Tools

- [Bootstrap Icons](https://icons.getbootstrap.com/) — icon library used throughout the UI

### Code

- [Django documentation](https://docs.djangoproject.com/en/5.2/) — referenced throughout for ORM, views, forms, authentication and deployment
- [Stripe documentation](https://stripe.com/docs) — referenced for PaymentIntent flow, Stripe.js card element and webhook event handling
- [Whitenoise documentation](https://whitenoise.readthedocs.io/) — referenced for static file configuration
- [Cloudinary documentation](https://cloudinary.com/documentation/django_integration) — referenced for media storage configuration
- Bootstrap 5 CDN components used for grid, navbar, cards, forms and pagination

### Tools and Platforms

- [GitHub](https://github.com) — version control and repository hosting
- [Heroku](https://heroku.com) — cloud deployment platform
- [Neon](https://neon.tech) — serverless PostgreSQL hosting
- [Cloudinary](https://cloudinary.com) — cloud media storage
- [Stripe](https://stripe.com) — payment processing

### Acknowledgements

_(To be completed.)_
