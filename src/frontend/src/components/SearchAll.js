import React, { useState, useEffect } from "react";
import { Input, InputAdornment } from "@material-ui/core";
import Search from "@material-ui/icons/Search";
import { useQuery } from "@apollo/react-hooks";
import { gql } from "apollo-boost";
import BillList from "./BillList";
import DonorList from "./DonorList";
import LegislatorList from "./LegislatorList";
import SimpleTabs from "./SimpleTabs";
import { useHistory, useParams } from "react-router-dom";
import CustomLink from "./CustomLink";
import useDebounce from "./useDebounce";

const ALL_SEARCH = gql`
  query Legislator($name: String) {
    legislators(name_Icontains: $name) {
      totalCount
    }
    bills(title_Icontains: $name) {
      totalCount
    }
    donors(fullName_Icontains: $name) {
      totalCount
    }
  }
`;

const LEG_SEARCH = gql`
  query LegislatorSearch(
    $first: Int
    $last: Int
    $after: String
    $before: String
    $name: String
  ) {
    legislators(
      first: $first
      last: $last
      after: $after
      before: $before
      name_Icontains: $name
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

const BILL_SEARCH = gql`
  query BillsSearch(
    $first: Int
    $last: Int
    $after: String
    $before: String
    $name: String
  ) {
    bills(
      title_Icontains: $name
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

const DONOR_SEARCH = gql`
  query DonorsSearch(
    $first: Int
    $last: Int
    $after: String
    $before: String
    $name: String
  ) {
    donors(
      first: $first
      last: $last
      after: $after
      before: $before
      fullName_Icontains: $name
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

export function SearchResults() {
  const { searchQuery } = useParams();
  const gqlVariables = { name: searchQuery };
  const { data } = useQuery(ALL_SEARCH, {
    variables: gqlVariables
  });

  let startTabIdx = 0;
  if (data && data.bills.totalCount) {
    if (!data.legislators.totalCount) {
      startTabIdx = 1;
      if (!data.donors.totalCount) {
        startTabIdx = 2;
      }
    }
  }
  return (
    <div className="detail-page">
      {searchQuery && data && <CustomLink to="/"> ← Clear Search</CustomLink>}
      {searchQuery && data && (
        <SimpleTabs
          startTabIdx={startTabIdx}
          tabs={[
            {
              label: `Legislators (${data.legislators.totalCount})`,
              content: (
                <div>
                  <LegislatorList
                    gqlVariables={gqlVariables}
                    gqlQuery={LEG_SEARCH}
                  />
                </div>
              )
            },
            {
              label: `Bills (${data.bills.totalCount})`,
              content: (
                <div>
                  <BillList
                    gqlVariables={gqlVariables}
                    gqlQuery={BILL_SEARCH}
                  />
                </div>
              )
            },
            {
              label: `Donors (${data.donors.totalCount})`,
              content: (
                <div>
                  <DonorList
                    gqlVariables={gqlVariables}
                    gqlQuery={DONOR_SEARCH}
                  />
                </div>
              )
            }
          ]}
        />
      )}
    </div>
  );
}

function SearchAll() {
  const history = useHistory();
  const searchQuery = history.location.pathname.split("/searchAll/")[1];
  const [searchVal, setSearchVal] = useState(searchQuery);
  useEffect(() => {
    setSearchVal(searchQuery);
  }, [searchQuery]);
  const debouncedSearchTerm = useDebounce(searchVal, 500);
  useEffect(() => {
    if (debouncedSearchTerm) {
      history.push(`/searchAll/${debouncedSearchTerm}`);
    } else {
      if (history.location.pathname.includes("searchAll")) {
        history.push("/");
      }
    }
    setSearchVal(debouncedSearchTerm);
  }, [debouncedSearchTerm]);

  return (
    <div className="site-wide-search" style={{ margin: "1em 0" }}>
      <Input
        value={searchVal || ""}
        onChange={e => setSearchVal(e.target.value)}
        placeholder="Search"
        startAdornment={
          <InputAdornment position="start">
            <Search />
          </InputAdornment>
        }
        fullWidth
      />
      <SearchResults />
    </div>
  );
}

export default SearchAll;
