# How to write Issues

GitHub Issues are how you track work. Three templates are available in `.github/ISSUE_TEMPLATE/` and will appear when you click **New issue** on the repo:

- **Requirement** — something the system must do (links to `BR-N` in [Requirements](requirements.md))
- **User story** — a piece of functionality framed from the user's perspective
- **Bug** — something is broken

Below is one worked example for each.

---

## Example: Requirement

> **Title:** `BR-1: User authentication`
> **Labels:** `requirement`, `functional`, `must-have`

### Description

The system must let users register an account, log in, and log out securely.

### Acceptance criteria

- [ ] A new user can create an account with email + password
- [ ] Passwords are at least 8 characters and stored hashed (never plaintext)
- [ ] A logged-in user can log out from any page
- [ ] Failed login attempts return a generic error (no info about whether the email exists)

### Source

Comes from user flow UF-1 "Register an account" in [Design](design.md). Listed as BR-1 in [Requirements](requirements.md).

---

## Example: User story

> **Title:** `Add password strength indicator on registration form`
> **Labels:** `user-story`, `frontend`

### Story

> As a new user
> I want to see how strong my password is while typing it
> So that I know whether it will be accepted before I hit Register

### Acceptance criteria

- [ ] A coloured bar appears under the password field once the user starts typing
- [ ] Bar updates in real time: red (too short), yellow (acceptable), green (strong)
- [ ] If the password is shorter than 8 characters, the Register button is disabled

### Linked requirement

Implements part of [BR-1](#example-requirement).

### Estimate

Estimate: 3h

---

## Example: Bug

> **Title:** `Logout button does nothing on /profile page`
> **Labels:** `bug`

### Summary

Clicking the Logout button in the top-right corner has no effect when the user is on the `/profile` page. Works fine on other pages.

### Steps to reproduce

1. Log in as any user
2. Navigate to `/profile`
3. Click the Logout button in the top-right corner

### Expected behaviour

User is logged out and redirected to the landing page.

### Actual behaviour

Nothing happens. No network request is made (verified in DevTools). Console shows `Uncaught TypeError: Cannot read properties of undefined (reading 'csrfToken')` on click.

### Environment

- Version: `v0.4.0-2-gabc1234`
- macOS 14.5, Chrome 124
- Logged in as a regular (non-admin) user

---

## Tips

- **One thing per Issue.** If you find yourself writing "and also..." in the title, split it.
- **Reference requirements by ID.** Use `BR-1` or `NFR-2` in titles or bodies so the link to [Requirements](requirements.md) is obvious.
- **Close with a commit message.** Use GitHub keywords in your PR description: `Closes #12`. The Issue closes automatically when the PR merges.
- **Don't archive context.** If a discussion happens in a chat or call, paste a short summary into the Issue. Six months from now you won't remember.
