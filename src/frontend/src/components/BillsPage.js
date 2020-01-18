import React, { useState } from "react";
import DonutChart from "./DonutChart";
import BillList from "./BillList";
import FilterSection from "./FilterSection";
import { useQuery } from "@apollo/react-hooks";
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
    billClassificationStats {
      classification
      count
    }
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

  const [pageInfo, setPageInfo] = useState({ first: 10 });

  const { data } = useQuery(ALL_BILLS, {
    variables: { ...pageInfo, chamber, classification: classifications }
  });
  const { totalCount } = data ? data.bills : {};

  const billClassificationStats = data ? data.billClassificationStats : [];
  const classificationTags = billClassificationStats.map(d => ({
    name: capitalize(d.classification.split("-").join(" ")),
    value: d.classification,
    arrayName: "classification"
  }));
  const summaryData = billClassificationStats.map(d => ({
    name: capitalize(d.classification.split("-").join(" ")),
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
      <DonutChart data={summaryData} totalCount={totalCount} />
      <BillList
        data={data && data.bills}
        handleChangePage={setPageInfo}
        title="All Bills"
      />
    </div>
  );
}

export default BillsPage;
