import React, { useState } from "react";
import DonorList from "./DonorList";
import { gql } from "apollo-boost";
import { useQuery } from "@apollo/react-hooks";
import { Typography } from "@material-ui/core";
import DonutChart from "./DonutChart";
import FilterSection from "./FilterSection";
import { getQueryString } from "../utils";
import { useHistory } from "react-router-dom";

const ALL_DONORS = gql`
  query AllDonors(
    $first: Int
    $last: Int
    $after: String
    $before: String
    $state: String
  ) {
    donors(
      first: $first
      last: $last
      after: $after
      before: $before
      state_Icontains: $state
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
          fullName
          city
          state
          employer
          totalContributions
        }
      }
    }
  }
`;

const TX_DONORS = gql`
  {
    donors(state: "TX") {
      totalCount
    }
  }
`;

function DonorsPage() {
  const inStateData = useQuery(TX_DONORS);
  const [listData, setListData] = useState();
  const history = useHistory();
  const queryObj = getQueryString(history);
  let state;
  if (queryObj["TX"]) {
    if (queryObj["TX"]) {
      state = "TX";
    }
  }

  let summaryData = [];

  if (inStateData.data && listData) {
    summaryData = [
      { name: "In state", value: inStateData.data.donors.totalCount },
      {
        name: "Out of state",
        value: listData.donors.totalCount - inStateData.data.donors.totalCount
      }
    ];
  }

  return (
    <div>
      <FilterSection
        title={
          <Typography variant="h6" style={{ minWidth: "150px" }}>
            Texas Donors
          </Typography>
        }
        tags={[{ name: "In state", value: "TX" }]}
      />
      <div className="two-column">
        <DonutChart
          data={summaryData}
          totalCount={listData ? listData.donors.totalCount : 0}
          totalText={"Donors"}
        />
        <DonorList
          gqlQuery={ALL_DONORS}
          title="Donors"
          onDataFetched={setListData}
          gqlVariables={{ state }}
        />
      </div>
    </div>
  );
}

export default DonorsPage;
