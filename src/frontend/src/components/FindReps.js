// Imports
import React, { useState } from "react";
import Autocomplete from "react-google-autocomplete";
import queryString from "query-string";
import { Typography } from "@material-ui/core";
import Script from "react-load-script";
import { useHistory } from "react-router-dom";
import { setQueryString, getQueryString, getDebugQuery } from "../utils";
import { useQuery } from "@apollo/react-hooks";
import { gql } from "apollo-boost";
import LegislatorsList from "./LegislatorList";

const GOOGLE_API = process.env.REACT_APP_GOOGLE_API_KEY;

const GET_LEG_BY_DISTRICT = gql`
  query Legislator($district: Int, $chamber: String) {
    legislators(district: $district, chamber_Icontains: $chamber) {
      edges {
        node {
          pk
          name
          party
          chamber
          photoUrl
          url
          district
        }
      }
    }
    ${getDebugQuery()}
  }
`;

function FindRepResults() {
  const history = useHistory();
  const query = getQueryString(history);
  const houseData = useQuery(GET_LEG_BY_DISTRICT, {
    variables: { district: query.house || 0, chamber: "house" },
  });
  const senateData = useQuery(GET_LEG_BY_DISTRICT, {
    variables: { district: query.senate || 0, chamber: "senate" },
  });
  if (!houseData.data || !senateData.data) return null;
  const totalCount =
    houseData.data.legislators.edges.length +
    senateData.data.legislators.edges.length;
  const edges = [
    ...houseData.data.legislators.edges,
    ...senateData.data.legislators.edges,
  ];
  if (!totalCount && Object.keys(query).length)
    return (
      <div style={{ marginTop: "1rem", opacity: 0.5 }}>
        None found, make sure the address is specific enough
      </div>
    );
  if (!totalCount) return null;

  return (
    <LegislatorsList
      data={{
        edges,
        totalCount,
      }}
    />
  );
}

export default function FindReps() {
  const [isLoaded, setIsLoaded] = useState(false);
  const history = useHistory();
  return (
    <div style={{ marginTop: "1rem" }}>
      <Typography variant="h6">Find Your Representatives</Typography>
      <Script
        url={`https://maps.googleapis.com/maps/api/js?key=${GOOGLE_API}&libraries=places`}
        onLoad={() => setIsLoaded(true)}
      />
      {isLoaded && (
        // giving the classes copied from the output make consistent with the react material ui components
        <div
          style={{ marginTop: "1rem" }}
          className="MuiInputBase-root MuiInput-root MuiInput-underline MuiInputBase-fullWidth MuiInput-fullWidth MuiInputBase-adornedStart"
        >
          <Autocomplete
            className="MuiInputBase-input MuiInput-input MuiInputBase-inputAdornedStart"
            onPlaceSelected={({ formatted_address }) => {
              const params = {
                key: GOOGLE_API,
                address: formatted_address,
                includeOffices: false,
                roles: ["legislatorUpperBody", "legislatorLowerBody"],
              };
              fetch(
                `https://www.googleapis.com/civicinfo/v2/representatives?${queryString.stringify(
                  params
                )}`
              )
                .then((res) => res.json())
                .then((res) => {
                  if (!res.divisions) return;
                  let house = "";
                  let senate = "";
                  Object.values(res.divisions).forEach((str) => {
                    if (str.name.includes("House")) {
                      house = str.name
                        .replace("Texas State House district", "")
                        .trim();
                    }
                    if (str.name.includes("Senate")) {
                      senate = str.name
                        .replace("Texas State Senate district", "")
                        .trim();
                    }
                  });
                  setQueryString({ house, senate }, history);
                });
            }}
            types={["address"]}
          />
        </div>
      )}
      <FindRepResults />
    </div>
  );
}
