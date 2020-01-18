import React, { useState } from "react";
import TexasDistrictMap from "./TexasDistrictMap";
import { useQuery } from "@apollo/react-hooks";
import { gql } from "apollo-boost";
import { getQueryString } from "../utils";
import FilterSection from "./FilterSection";
import LegislatorList from "./LegislatorList";
import { useHistory } from "react-router-dom";
import { Typography } from "@material-ui/core";

const ALL_LEG = gql`
  query Legislator(
    $chamber: String
    $party: String
    $first: Int
    $last: Int
    $after: String
    $before: String
  ) {
    legislators(
      party: $party
      chamber_Icontains: $chamber
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
          name
          party
          chamber
          district
          photoUrl
        }
      }
    }
  }
`;

function LegislatorsPage() {
  const history = useHistory();
  const [pageInfo, setPageInfo] = useState({ first: 10 });
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

  let party;
  if (queryObj["D"] !== queryObj["R"]) {
    if (queryObj["D"]) {
      party = "D";
    }
    if (queryObj["R"]) {
      party = "R";
    }
  }

  const { data } = useQuery(ALL_LEG, {
    variables: { chamber, party, first: 10, ...pageInfo }
  });
  return (
    <div>
      <FilterSection
        title={<Typography variant="h6">Texas Legislators</Typography>}
        tags={[
          { name: "House", value: "HOUSE" },
          { name: "Senate", value: "SENATE" },
          { name: "Democrat", value: "D" },
          { name: "Republican", value: "R" }
        ]}
      />
      <TexasDistrictMap chamber={chamber} />
      <LegislatorList
        title={"All Legislators"}
        data={data && data.legislators}
        handleChangePage={setPageInfo}
      />
    </div>
  );
}

export default LegislatorsPage;
