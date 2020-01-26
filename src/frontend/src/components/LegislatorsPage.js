import React, { useState, useEffect } from "react";
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
  const queryObj = getQueryString(history);

  const chamber = queryObj.chamber;
  const party = queryObj.party;

  return (
    <div>
      <FilterSection
        title={<Typography variant="h6">Texas Legislators</Typography>}
        tags={{
          chamber: [
            { name: "House", value: "HOUSE" },
            { name: "Senate", value: "SENATE" }
          ],
          party: [
            { name: "Democrat", value: "D" },
            { name: "Republican", value: "R" }
          ]
        }}
      />
      <div className="two-column">
        <TexasDistrictMap chamber={chamber} style={{ flexGrow: 1 }} />
        <LegislatorList
          title={"All Legislators"}
          gqlQuery={ALL_LEG}
          gqlVariables={{ chamber, party }}
        />
      </div>
    </div>
  );
}

export default LegislatorsPage;
