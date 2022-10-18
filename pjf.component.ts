interface Bidder {
  isSelectAllChecked: boolean;
  isSelected: boolean;
  bidderName: string;
  isWinner: boolean;
}

interface LineItem {
  bidders: Bidder[];
  selectedWinnersList: string[];
  selectedWinnerValue?: string;
  modifyWinnerInMultiVendorScenario: boolean;
  systemCalculatedBidderName?: string;
}

class PJFComponent {
  winnerCount = 0;
  bidderAnalysisGridLineItems: LineItem[] = [];

  checkWinnerFlag(bidder: VendorProposal): void {
    if (
      bidder &&
      Array.isArray(this.bidderAnalysisGridLineItems) &&
      this.bidderAnalysisGridLineItems.length > 0
    ) {
      this.winnerCount = 0;
      this.bidderAnalysisGridLineItems.forEach((lineItem, index) => {
        if (lineItem.bidders && lineItem.bidders.length > 0) {
          if (!lineItem.selectedWinnersList) {
            lineItem.selectedWinnersList = [] as Array<string>;
          }
          lineItem.bidders.forEach(vendor => {
            if (bidder.bidderName === vendor.bidderName) {
              if (vendor.isWinner) {
                vendor.isSelected = true;
                this.winnerCount++;
                if (
                  lineItem.selectedWinnersList &&
                  lineItem.selectedWinnersList.length > 0
                ) {
                  const duplicateCheck = lineItem.selectedWinnersList.filter(
                    x => x === vendor.bidderName
                  )[0]; // Existing Bidder
                  if (duplicateCheck === undefined) {
                    lineItem.selectedWinnersList.push(vendor.bidderName);
                  }
                } else {
                  lineItem.selectedWinnersList.push(vendor.bidderName); // First time
                }
              } else {
                vendor.isSelected = false;
                bidder.isSelectAllChecked = false;
                vendor.isSelectAllChecked = false;
                if (
                  lineItem.selectedWinnersList &&
                  lineItem.selectedWinnersList.length > 0
                ) {
                  lineItem.selectedWinnersList.forEach((winner, indx) => {
                    if (winner === vendor.bidderName) {
                      lineItem.selectedWinnersList.splice(indx, 1);
                    }
                  });
                }
              }
            }
          });
        }
        lineItem.selectedWinnersList.forEach((winner, indx) => {
          if (indx === 0 && lineItem.selectedWinnersList.length === 1) {
            lineItem.selectedWinnerValue = winner;
          } else if (indx === 0 && lineItem.selectedWinnersList.length > 1) {
            lineItem.selectedWinnerValue = winner + ", ";
          } else if (
            indx > 0 &&
            indx <= lineItem.selectedWinnersList.length - 2
          ) {
            lineItem.selectedWinnerValue += winner + ", ";
          } else if (indx === lineItem.selectedWinnersList.length - 1) {
            lineItem.selectedWinnerValue += winner;
          }
        });

        if (
          lineItem.selectedWinnerValue &&
          lineItem.systemCalculatedBidderName &&
          lineItem.selectedWinnerValue !== lineItem.systemCalculatedBidderName
        ) {
          lineItem.modifyWinnerInMultiVendorScenario = true;
        } else {
          lineItem.modifyWinnerInMultiVendorScenario = false;
        }
      });

      // if winners count equal to Line Items count, then make Select All as true
      if (this.winnerCount === this.bidderAnalysisDetails.length) {
        bidder.isSelectAllChecked = true;
        bidder.isSelected = true;
      } else {
        bidder.isSelectAllChecked = false;
      }
    }
  }

  checkWinnerFlag2(bidder: Bidder): void {
    const linesAssignedToBidder = this.bidderAnalysisGridLineItems.filter(
      lineItem =>
        lineItem.bidders.some(vendor => vendor.bidderName === bidder.bidderName)
    );

    this.bidderAnalysisGridLineItems.forEach(lineItem => {
      const winners: Set<string> = new Set();
      lineItem.bidders.forEach(vendor => {
        if (bidder.bidderName === vendor.bidderName) {
          if (vendor.isWinner) {
            vendor.isSelected = true;
            winners.add(vendor.bidderName);
          } else {
            vendor.isSelected = false;
            bidder.isSelectAllChecked = false;
            vendor.isSelectAllChecked = false;
            winners.delete(vendor.bidderName);
          }
        }
      });

      this.winnerCount = winners.size;
      lineItem.selectedWinnersList = [...winners];
      lineItem.selectedWinnerValue = lineItem.selectedWinnersList.join(", ");
      lineItem.modifyWinnerInMultiVendorScenario = !!(
        lineItem.selectedWinnerValue &&
        lineItem.systemCalculatedBidderName &&
        lineItem.selectedWinnerValue !== lineItem.systemCalculatedBidderName
      );
    });

    // if winners count equal to Line Items count, then make Select All as true
    if (this.winnerCount === this.bidderAnalysisDetails.length) {
      bidder.isSelectAllChecked = true;
      bidder.isSelected = true;
    } else {
      bidder.isSelectAllChecked = false;
    }
  }
}
