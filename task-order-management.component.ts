import { forkJoin, of } from "rxjs";

class TaskOrderManagement {
  loadDropDownValues() {
    return forkJoin([
      of([
        { isActive: true, name: "timiza" },
        { isActive: false, name: "unitaid" },
      ]),
      of(["cost reimbursable", "labor hour"]),
      of(["nairobi", "dc"]),
    ]);
  }

  initializeTaskOrder(): void {
    this.loadDropDownValues().subscribe(([res1, res2, res3]) => {
      const fundingSources = res1.filter(source => source.isActive);
      const pricings = res2;
      const offices = res3;
    });
  }
}
