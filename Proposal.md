# The Big Idea

## Title
**MLB Hitter Lookup — Flask App**

## Goal
Enter an MLB player’s name → return hitting stats (season or career) using **pybaseball**.

## MVP
Text input → resolve name → ID → fetch core batting stats → return as a simple table/JSON.

## Stretch
- Team-by-team splits endpoint  
- Season selector  
- Basic chart (optional)  
- Simple caching  

---

## Learning Objectives

### Shared
- Build a small Flask service  
- Fetch/clean sports data with **pandas**  
- Document & test  

### Individual
- **Jack:** deep dive into flask routes & error handling and Output formatting (table/JSON), optional plots  
- **Sophia:** deep dive into data layer (pybaseball, caching), working with different libraries

---

## Implementation Plan

### Libraries
`Flask`, `pybaseball`, `pandas`, `numpy` (+ `matplotlib` optional), `requests` (if needed)

### Endpoints
- `GET /` → search form or minimal input page  
- `POST /player` → name → ID, fetch season/career stats, return table/JSON  
- `GET /player/<id>/splits` (stretch) → vs-team splits  

### Data Flow
`name` → candidate IDs → pick one → fetch stats → clean columns → return  

### Caching
JSON files in `data/` keyed by *(player_id, season, scope)*  

---

## Project Schedule (2–3 weeks)

**Week 1:** Flask skeleton, name→ID, basic fetch, return raw table/JSON  
**Week 2:** Robust errors, caching, small tests, finalize MVP  
**Week 3:** Splits endpoint, optional chart, polish README  

---

## Collaboration Plan

**GitHub Workflow:** feature branches → PRs → code review; short stand-ups; light Agile sprints.  

**Roles:**
- **Jack:** backend/routes and output/plots
- **Sophia:** data services and QA/docs


**Why this structure:** parallelizable tasks, quick feedback, fewer merge conflicts  

---

## Risks & Limitations
- Name collisions (disambiguation needed)  
- External data/library changes → mitigate with caching & CSV fallback  
- Scope creep on visuals — protect MVP first  
- Environment setup (ensure `requirements.txt`)  

---

## Additional Course Content Helpful
- Quick Flask patterns (routing, request handling)  
- Simple caching patterns  
- Basic testing (`pytest` / mocks)

