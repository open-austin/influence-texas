import React, { useState } from "react";
import DonutChart from "./DonutChart";
import BillList from "./BillList";
import FilterSection from "./FilterSection";
import { gql } from "apollo-boost";
import { getQueryString, capitalize } from "../utils";
import { useHistory } from "react-router-dom";
import { Typography } from "@material-ui/core";

const ALL_BILLS = gql`
  query AllBills(
    $chamber: String
    $classification: [String]
    $first: Int
    $last: Int
    $after: String
    $before: String
  ) {
    bills(
      chamber_Icontains: $chamber
      classification: $classification
      first: $first
      last: $last
      after: $after
      before: $before
    ) {
      totalCount
      pageInfo {
        hasNextPage
        hasPreviousPage
        startCursor
        endCursor
      }
      edges {
        cursor
        node {
          pk
          chamber
          billId
          title
        }
      }
    }
    billClassificationStats {
      name
      count
    }
  }
`;

function BillsPage() {
  const history = useHistory();
  const queryObj = getQueryString(history);
  let chamber;
  if (queryObj["HOUSE"] !== queryObj["SENATE"]) {
    if (queryObj["HOUSE"]) {
      chamber = "HOUSE";
    }
    if (queryObj["SENATE"]) {
      chamber = "SENATE";
    }
  }
  const classifications = queryObj.classification || [];
  const [listData, setListData] = useState();

  const billClassificationStats = listData
    ? listData.billClassificationStats
    : [];
  const classificationTags = billClassificationStats.map(d => ({
    name: capitalize(d.name.split("-").join(" ")),
    value: d.name,
    arrayName: "classification"
  }));
  const summaryData = billClassificationStats.map(d => ({
    name: capitalize(d.name.split("-").join(" ")),
    value: d.count
  }));

  return (
    <div>
      <FilterSection
        title={
          <Typography variant="h6" style={{ minWidth: "150px" }}>
            Texas Bills
          </Typography>
        }
        tags={[
          { name: "House", value: "HOUSE" },
          { name: "Senate", value: "SENATE" },
          ...classificationTags
        ]}
      />
      <div className="two-column">
        <DonutChart
          data={summaryData}
          totalCount={listData ? listData.bills.totalCount : 0}
          totalText="Bills"
        />
        <BillList
          gqlQuery={ALL_BILLS}
          gqlVariables={{ chamber, classification: classifications }}
          title="All Bills"
          onDataFetched={setListData}
        />
      </div>
    </div>
  );
}

export default BillsPage;
