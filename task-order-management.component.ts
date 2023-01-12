import { forkJoin, of } from "rxjs";

class TaskOrderManagement {
  loadDropDownValues() {
    return forkJoin([
      of(["source1", "source2"]),
      of(["price1", "price2"]),
      of(["office1", "office2"]),
    ]);
  }

  initializeTaskOrder(): void {
    this.loadDropDownValues().subscribe(([res1, res2, res3]) => {
      const fundingSources = res1.map(source => source.toUpperCase());
      const pricings = res2;
      const offices = res3;
    });
  }
}
