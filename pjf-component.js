class PJFComponent {
  bidderEvaluationResults = [
    // taken from S020784 in PROD
    {
      evaluation: [
        {
          score: 4,
          weightPercentage: 15,
        },
        {
          score: 3.75,
          weightPercentage: 60,
        },
        {
          score: 5,
          weightPercentage: 25,
        },
      ],
      bidderName: "FIDA RAMSINA Pelagie",
    },
    {
      evaluation: [
        {
          score: 4,
          weightPercentage: 15,
        },
        {
          score: 3.5,
          weightPercentage: 60,
        },
        {
          score: 5,
          weightPercentage: 25,
        },
      ],
      bidderName: "Esendege Luke Fotabe",
    },
    {
      evaluation: [
        {
          score: 1,
          weightPercentage: 15,
        },
        {
          score: 4.18,
          weightPercentage: 60,
        },
        {
          score: 5,
          weightPercentage: 25,
        },
      ],
      bidderName: "WOUAFACK KENFACK Victorien",
    },
    {
      evaluation: [
        {
          score: 4,
          weightPercentage: 15,
        },
        {
          score: 3.33,
          weightPercentage: 60,
        },
        {
          score: 5,
          weightPercentage: 25,
        },
      ],
      bidderName: "PEMBOUONG Gynette",
    },
    {
      evaluation: [
        {
          score: 1,
          weightPercentage: 15,
        },
        {
          score: 3.93,
          weightPercentage: 60,
        },
        {
          score: 5,
          weightPercentage: 25,
        },
      ],
      bidderName: "TAJO DJIDJOU Brice",
    },
    {
      evaluation: [
        {
          score: 4,
          weightPercentage: 15,
        },
        {
          score: 2.43,
          weightPercentage: 60,
        },
        {
          score: 5,
          weightPercentage: 25,
        },
      ],
      bidderName: "MUSA HAMMADOU JAOURO",
    },
  ];
  allFinalScoresList;
  allContractPricesList;
  bidderCount = 1;
  bidderAssessmentDetails = [
    {
      vendorId: 1,
      isDocumentSubmitted: true,
      isResponsive: true,
      totalPrice: 3600000,
    },
    {
      vendorId: 4,
      isDocumentSubmitted: true,
      isResponsive: true,
      totalPrice: 3600000,
    },
    {
      vendorId: 5,
      isDocumentSubmitted: true,
      isResponsive: true,
      totalPrice: 3600000,
    },
    {
      vendorId: 6,
      isDocumentSubmitted: true,
      isResponsive: true,
      totalPrice: 3600000,
    },
    {
      vendorId: 7,
      isDocumentSubmitted: true,
      isResponsive: true,
      totalPrice: 3600000,
    },
    {
      vendorId: 8,
      isDocumentSubmitted: true,
      isResponsive: true,
      totalPrice: 3600000,
    },
  ];
  solicitationEntryPageLineItemDetails = [
    { extendedPriceUSD: 51315 },
    { extendedPriceUSD: 2612.4 },
    { extendedPriceUSD: 4043 },
    { extendedPriceUSD: 16794 },
  ];
  bidderSolicitationDetails = [
    { vendorId: 1, bidderName: "bidder1" },
    { vendorId: 2, bidderName: "bidder2" },
  ];
  numberOfCriteria = 3;
  evaluationCriteriaDetails = [
    {
      id: 1,
      evaluationCriteria: "past performance",
      criteriaScore: undefined,
      weightPercentage: 15,
      evaluationCriteriaId: 1,
    },
    {
      id: 2,
      evaluationCriteria: "qualifications",
      criteriaScore: undefined,
      weightPercentage: 60,
      evaluationCriteriaId: 2,
    },
    {
      id: 3,
      evaluationCriteria: "price",
      criteriaScore: undefined,
      weightPercentage: 25,
      evaluationCriteriaId: 3,
    },
  ];

  resetAllFlags() {}

  setSolicitationBidderAfterReturnToDraft() {
    const missingCriteria = this.bidderSolicitationDetails
      .filter(
        evalCriteria =>
          !this.bidderAssessmentDetails.some(
            x => x.vendorId === evalCriteria.vendorId
          )
      )
      .map(evalCriteria => {
        const { bidderName, vendorId } = evalCriteria;
        return { bidderName, vendorId };
      });
    this.bidderAssessmentDetails = [
      ...this.bidderAssessmentDetails,
      ...missingCriteria,
    ];
  }

  aggregateAllFinalScores() {
    if (this.bidderEvaluationResults.length === 0) {
      return this.allFinalScoresList;
    }

    this.allFinalScoresList = this.bidderEvaluationResults
      .map(evaluation =>
        evaluation.finalScore > 0 ? evaluation.finalScore : 0
      )
      .sort((a, b) => b - a)
      .slice(0, this.bidderCount);

    return this.allFinalScoresList;
  }

  aggregateAllContractPrice() {
    if (
      this.bidderAssessmentDetails &&
      this.bidderAssessmentDetails.length > 0
    ) {
      this.allContractPricesList = [];
      this.bidderAssessmentDetails.forEach(bidder => {
        if (
          bidder.isDocumentSubmitted &&
          bidder.isResponsive &&
          bidder.totalPrice >= 0
        ) {
          this.allContractPricesList.push(bidder.totalPrice);
        }
      });
    }
  }

  aggregateAllContractPrice2() {
    this.allContractPricesList = this.bidderAssessmentDetails
      .filter(bidder => {
        return (
          bidder.isDocumentSubmitted &&
          bidder.isResponsive &&
          bidder.totalPrice >= 0
        );
      })
      .map(bidder => bidder.totalPrice);
  }

  setMultiWinnersFlag() {
    this.aggregateAllFinalScores();
    if (
      this.allFinalScoresList?.length === 0 ||
      !(0 < this.bidderCount <= this.bidderEvaluationResults.length)
    ) {
      return;
    }

    this.resetAllFlags();
    const winningBidders = new Set();
    this.bidderEvaluationResults.forEach(bidder => {
      if (this.allFinalScoresList.includes(bidder.finalScore)) {
        bidder.isMultipleWinnersAllowed = true;
        winningBidders.add(bidder.bidderName);
      }
    });
    this.bvScenarioWinningBiddersList = [...winningBidders];
  }

  calculateTotalContractAmount() {
    if (
      this.bidderAssessmentDetails &&
      this.bidderAssessmentDetails.length > 0
    ) {
      this.bidderAssessmentDetails.forEach(ele => {
        if (ele.isWinner) {
          this.winnerTotalContractAmount =
            ele.totalPrice * this.getXchangeRateById(ele.currencyId);
        }
      });
    }
  }

  calculateTotalContractAmount2() {
    this.winnerTotalContractAmount = this.bidderAssessmentDetails
      .find(ele => ele.isWinner)
      .reduce(
        (total, ele) =>
          ele.totalPrice * this.getXchangeRateById(ele.currencyId) + total,
        0
      );
  }

  calculateTotalSolicitationLineItemsAmt() {
    this.solicitationEntryPageLineItemsTotalAmt =
      this.solicitationEntryPageLineItemDetails.reduce(
        (total, lineItem) => lineItem.extendedPriceUSD + total,
        0
      );
  }

  checkMultipleContractsOnSingleItemFlags() {
    // To check SelectAll is checked or not,
    if (
      Array.isArray(this.bidderAnalysisGridLineItems) &&
      this.bidderAnalysisGridLineItems.length > 0
    ) {
      this.bidderAnalysisGridLineItems.forEach(lineItem => {
        if (lineItem.bidders && lineItem.bidders.length > 0) {
          lineItem.bidders.forEach(bidder => {
            // for each bidder, check isWinner flag,
            this.checkWinnerFlag(bidder);
          });
        }
      });
    }
  }

  checkMultipleContractsOnSingleItemFlags2() {
    this.bidderAnalysisGridLineItems?.forEach(lineItem =>
      lineItem.bidders?.forEach(this.checkWinnerFlag)
    );
  }

  checkWinnerFlag(bidder) {
    if (
      bidder &&
      Array.isArray(this.bidderAnalysisGridLineItems) &&
      this.bidderAnalysisGridLineItems.length > 0
    ) {
      this.winnerCount = 0;
      this.bidderAnalysisGridLineItems.forEach(lineItem => {
        if (lineItem.bidders && lineItem.bidders.length > 0) {
          if (!lineItem.selectedWinnersList) {
            lineItem.selectedWinnersList = [];
          }
          lineItem.bidders.forEach(vendor => {
            if (bidder.bidderName === vendor.bidderName) {
              if (vendor.isWinner) {
                // && lineItem.justificationForNotSelectingVendor
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

  checkWinnerFlag2(bidder) {
    if (!bidder || this.bidderAnalysisGridLineItems?.length === 0) return;

    this.winnerCount = lineItem.bidders.reduce(
      (count, vendor) => count + (vendor.isWinner ? 1 : 0),
      0
    );
    this.bidderAnalysisGridLineItems.forEach(lineItem => {
      if (lineItem.bidders?.length > 0) {
        if (!lineItem.selectedWinnersList) {
          lineItem.selectedWinnersList = [];
        }
        const vendor = lineItem.bidders.find(
          v => v.bidderName === bidder.bidderName
        );
        vendor.isSelected = vendor.isWinner;

        const selectedWinners = new Set();
        if (vendor.isWinner) {
          selectedWinners.add(vendor.bidderName);
        } else {
          bidder.isSelectAllChecked = false;
          vendor.isSelectAllChecked = false;
          selectedWinners.delete(vendor.bidderName);
        }
        lineItem.selectedWinnersList = [...selectedWinners];
      }
      lineItem.selectedWinnersList = lineItem.selectedWinnersList.join(", ");
      lineItem.modifyWinnerInMultiVendorScenario =
        lineItem.selectedWinnerValue !== lineItem.systemCalculatedBidderName;
    });

    bidder.isSelectAllChecked =
      this.winnerCount === this.bidderAnalysisDetails.length;
    if (bidder.isSelectAllChecked) {
      bidder.isSelected = true;
    }
  }

  isFinalScoreCalculated() {
    this.isAnyOfBidderFinalScoreZero =
      this.bidderEvaluationResults.some(item => !item.finalScore) ?? false;
    return this.isAnyOfBidderFinalScoreZero;
  }

  calculateFinalScore(dataItem) {
    const evaluations = dataItem.evaluation?.splice(0, this.numberOfCriteria);
    if (!evaluations?.every(item => item?.score)) return;

    const finalScore = evaluations.reduce((total, curr) => {
      return total + (curr.score * curr.weightPercentage) / 100;
    }, 0);

    dataItem.finalScore =
      Math.round(Math.pow(10, 2) * finalScore) / Math.pow(10, 2);
  }
}

const pjf = new PJFComponent();
