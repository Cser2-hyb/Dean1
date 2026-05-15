# ROADMAP - Event Equipment Rental & Logistics

## 1. Project overview

Subject: PFP191 - Programming Fundamentals with Python

Topic 06: Event Equipment Rental & Logistics

Goal: Build a Python console application to manage event equipment and rental orders.

Main requirements:
- Use OOP with `Equipment` and `Rental` classes.
- Use `list` and `dict` for storage while the program is running.
- Save and load data using CSV or text files.
- Use `try-except` for input validation.
- Create a professional console menu.
- Organize code into multiple `.py` modules.
- Use private attributes and property decorators.
- Submit source code, technical report PDF, and presentation slides.

---

## 2. Team roles and workload sharing

### Cser2-hyb - Leader / Main Developer / Main Tester

Responsibilities:
- Manage GitHub repository and project board.
- Create project structure.
- Build and review the main menu.
- Implement or review rental logic.
- Integrate all modules.
- Review code and fix bugs.
- Test important features before marking tasks as Done.
- Lead final demo.

Assigned issues:
- #1 Setup project structure and README
- #3 Create Rental class with fee and penalty logic
- #6 Build Rental Management service and menu
- #8 Add exception handling and input validation
- #9 Prepare sample data and manual test cases

Shared testing with Titanrz:
- Test #2 Equipment class
- Test #4 CSV file loading and saving
- Test #5 Equipment Management menu
- Test #6 Rental Management menu
- Test #7 Data analysis and sorting functions

---

### Titanrz - Coder Member / Co-Tester

Responsibilities:
- Implement equipment-related code.
- Implement CSV file loading and saving.
- Implement sorting and data analysis.
- Help test the system with Cser2-hyb.
- Test the features after coding before asking for leader review.
- Help reduce the leader's testing workload.

Assigned coding issues:
- #2 Create Equipment class with validation
- #4 Implement CSV file loading and saving
- #5 Build Equipment Management service and menu
- #7 Implement data analysis and sorting functions

Shared testing issues:
- #2 Test Equipment class validation
- #4 Test CSV load/save after restart
- #5 Test add/search/update equipment
- #6 Test rental workflow with Cser2-hyb
- #7 Test sorting and grouping functions
- #8 Help test invalid input cases
- #9 Help prepare and run manual test cases

---

### nguyenphanleha2k7-hub - Report Member

Responsibilities:
- Write final report.
- Create class diagram.
- Create flowchart.
- Add screenshots from the running program.
- Explain project objective, architecture, features, file storage, validation, and testing.

Assigned issue:
- #10 Write final report

---

### NTVien207 - Slide / Demo Support Member

Responsibilities:
- Create presentation slides.
- Prepare speaking notes for presentation.
- Help collect screenshots from the running program.
- Help prepare demo script.
- Support manual testing if needed.

Assigned issue:
- #11 Create presentation slides and demo script

Note: NTVien207 must accept the GitHub invitation before being assigned directly.

---

## 3. Updated task assignment table

| Issue | Task | Main owner | Support / Test |
|---|---|---|---|
| #1 | Setup project structure and README | Cser2-hyb | Titanrz reviews structure |
| #2 | Create Equipment class with validation | Titanrz | Cser2-hyb tests |
| #3 | Create Rental class with fee and penalty logic | Cser2-hyb | Titanrz tests duration, fee, penalty |
| #4 | Implement CSV file loading and saving | Titanrz | Cser2-hyb tests restart/load/save |
| #5 | Build Equipment Management service and menu | Titanrz | Cser2-hyb tests add/search/update |
| #6 | Build Rental Management service and menu | Cser2-hyb | Titanrz tests rental flow |
| #7 | Implement data analysis and sorting functions | Titanrz | Cser2-hyb tests sorting results |
| #8 | Add exception handling and input validation | Cser2-hyb | Titanrz helps test invalid inputs |
| #9 | Prepare sample data and manual test cases | Cser2-hyb | Titanrz runs test cases together |
| #10 | Write final report | nguyenphanleha2k7-hub | Cser2-hyb provides screenshots/info |
| #11 | Create presentation slides and demo script | NTVien207 | Cser2-hyb provides demo flow |

---

## 4. Project folder structure

```text
event_equipment_rental/
├── main.py
├── models/
│   ├── equipment.py
│   └── rental.py
├── services/
│   ├── equipment_service.py
│   ├── rental_service.py
│   └── analysis_service.py
├── storage/
│   ├── file_handler.py
│   ├── equipment.csv
│   ├── rentals.csv
│   ├── rental_history.txt
│   └── maintenance_log.txt
├── utils/
│   ├── validators.py
│   └── time_utils.py
└── docs/
    ├── report.pdf
    └── slides.pptx
```

---

## 5. Development phases

### Phase 1 - Project setup

Tasks:
- Create folders and starter files.
- Add `README.md`.
- Create a simple `main.py`.
- Push structure to GitHub.

Related issue:
- #1

Owner:
- Cser2-hyb

Done when:
- `python main.py` runs without crashing.

---

### Phase 2 - Core OOP models

Tasks:
- Create `Equipment` class.
- Create `Rental` class.
- Use private attributes.
- Use property decorators.
- Add `to_dict()` and `from_dict()`.
- Validate invalid values.

Related issues:
- #2
- #3

Owners:
- #2 Equipment: Titanrz codes, Cser2-hyb tests.
- #3 Rental: Cser2-hyb codes, Titanrz tests.

Done when:
- Equipment and Rental objects can be created.
- Invalid data is rejected.
- Objects can be converted for CSV storage.

---

### Phase 3 - File I/O

Tasks:
- Implement `storage/file_handler.py`.
- Load equipment from `equipment.csv`.
- Load rentals from `rentals.csv`.
- Save data when the program exits.
- Create storage files if missing.
- Add rental history and maintenance logs.

Related issue:
- #4

Owner:
- Titanrz codes, Cser2-hyb tests restart/load/save.

Done when:
- Data is still available after restarting the program.

---

### Phase 4 - Equipment management

Tasks:
- Add new equipment.
- Search equipment by ID.
- Search equipment by status.
- Update equipment details.
- Show all equipment.
- Connect functions to menu.

Related issue:
- #5

Owner:
- Titanrz codes, Cser2-hyb tests add/search/update.

Done when:
- User can manage equipment from the menu.

---

### Phase 5 - Rental management

Tasks:
- Create rental order.
- Check equipment exists.
- Check equipment status is Available.
- Change status to Rented.
- Return equipment.
- Change status back to Available.
- Calculate rental fee.
- Calculate late penalty.

Related issue:
- #6

Owner:
- Cser2-hyb codes, Titanrz tests rental workflow.

Done when:
- Rental workflow works from the console menu.

---

### Phase 6 - Data analysis

Tasks:
- Sort equipment by hourly rental rate.
- Sort equipment by power rating.
- Sort rentals by duration.
- Sort rentals by client name.
- Group equipment by status.

Related issue:
- #7

Owner:
- Titanrz codes, Cser2-hyb tests output.

Done when:
- All analysis features work from the menu.

---

### Phase 7 - Validation and exception handling

Tasks:
- Validate menu choices.
- Validate numeric input.
- Validate client name.
- Validate rental time format.
- Validate start time before return time.
- Handle missing equipment ID.
- Handle unavailable equipment.

Related issue:
- #8

Owner:
- Cser2-hyb codes, Titanrz helps test invalid input cases.

Done when:
- Program does not crash on wrong input.

---

### Phase 8 - Testing, report, and slides

Tasks:
- Prepare sample data.
- Write at least 10 manual test cases.
- Run manual test cases with Cser2-hyb and Titanrz.
- Take screenshots.
- Write final report.
- Create class diagram.
- Create flowchart.
- Create presentation slides.
- Prepare demo script.

Related issues:
- #9
- #10
- #11

Owners:
- #9 Testing: Cser2-hyb + Titanrz.
- #10 Report: nguyenphanleha2k7-hub.
- #11 Slides: NTVien207.

Done when:
- Code, report PDF, and slides are ready.

---

## 6. Weekly timeline

### Week 1
- Finish GitHub setup.
- Finish project structure.
- Assign team roles.

### Week 2
- Finish `Equipment` and `Rental` classes.
- Titanrz and Cser2-hyb test both classes together.

### Week 3
- Finish CSV/Text file loading and saving.
- Titanrz tests load/save first, then Cser2-hyb reviews.

### Week 4
- Finish Equipment Management menu.
- Titanrz tests add/search/update, then Cser2-hyb reviews.

### Week 5
- Finish Rental Management menu.
- Cser2-hyb codes rental flow, Titanrz tests rental scenarios.

### Week 6
- Finish fee calculation, late penalty, and status updates.
- Titanrz helps test normal rental and late return cases.

### Week 7
- Finish sorting, grouping, validation, and error handling.
- Cser2-hyb and Titanrz run invalid input tests together.

### Week 8
- Finish testing, report draft, diagrams, and slides draft.
- Cser2-hyb and Titanrz provide screenshots and test results to report/slide members.

### Week 9
- Fix final bugs.
- Export report to PDF.
- Review slides.
- Practice presentation and demo.

---

## 7. Priority order

1. Project structure
2. Equipment class
3. Rental class
4. File I/O
5. Equipment management
6. Rental management
7. Validation and exception handling
8. Data analysis
9. Testing with Cser2-hyb + Titanrz
10. Report
11. Slides

---

## 8. Testing responsibility split

### Cser2-hyb tests
- Overall menu flow.
- Rental creation and return flow.
- Invalid rental times.
- Missing client name.
- Final integration before demo.

### Titanrz tests
- Equipment class validation.
- Equipment add/search/update.
- CSV load/save.
- Sorting by rental rate and power rating.
- Rental fee and late penalty together with Cser2-hyb.
- Invalid equipment status and unavailable equipment.

### Both test together
- Full demo from start to finish.
- Add equipment -> create rental -> return rental -> calculate fee -> check CSV.
- At least 10 manual test cases.

---

## 9. Final checklist

- [ ] Source code `.py` files completed
- [ ] Code organized into multiple modules
- [ ] `Equipment` class completed
- [ ] `Rental` class completed
- [ ] Private attributes used
- [ ] Property decorators used
- [ ] Equipment management completed
- [ ] Rental management completed
- [ ] Fee calculation completed
- [ ] Late penalty calculation completed
- [ ] Sorting functions completed
- [ ] Grouping by status completed
- [ ] CSV/Text storage completed
- [ ] Auto-load on startup completed
- [ ] Save on exit completed
- [ ] Try-except validation completed
- [ ] Test cases completed by Cser2-hyb and Titanrz
- [ ] Technical report PDF completed
- [ ] Class diagram completed
- [ ] Flowchart completed
- [ ] Presentation slides completed
- [ ] Demo script completed
