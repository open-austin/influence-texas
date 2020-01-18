import React, { useState, useEffect } from "react";
import { Input } from "@material-ui/core";
import { useQuery } from "@apollo/react-hooks";
import { gql } from "apollo-boost";
import BillList from "./BillList";
import DonorList from "./DonorList";
import LegislatorList from "./LegislatorList";
import SimpleTabs from "./SimpleTabs";
import InputAdornment from "@material-ui/core/InputAdornment";
import Search from "@material-ui/icons/Search";
import { useHistory, useParams } from "react-router-dom";

const ALL_SEARCH = gql`
  query Legislator($name: String) {
    legislators(name_Icontains: $name, first: 5) {
      totalCount
      edges {
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
    bills(title_Icontains: $name, first: 5) {
      totalCount
      edges {
        node {
          pk
          chamber
          billId
          title
        }
      }
    }
    donors(fullName_Icontains: $name, first: 5) {
      totalCount
      edges {
        node {
          pk
          city
          state
          employer
          fullName
          totalContributions
        }
      }
    }
  }
`;

// Our hook
export function useDebounce(value, delay) {
  // State and setters for debounced value
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(
    () => {
      // Set debouncedValue to value (passed in) after the specified delay
      const handler = setTimeout(() => {
        setDebouncedValue(value);
      }, delay);

      // Return a cleanup function that will be called every time ...
      // ... useEffect is re-called. useEffect will only be re-called ...
      // ... if value changes (see the inputs array below).
      // This is how we prevent debouncedValue from changing if value is ...
      // ... changed within the delay period. Timeout gets cleared and restarted.
      // To put it in context, if the user is typing within our app's ...
      // ... search box, we don't want the debouncedValue to update until ...
      // ... they've stopped typing for more than 500ms.
      return () => {
        clearTimeout(handler);
      };
    },
    // Only re-call effect if value changes
    // You could also add the "delay" var to inputs array if you ...
    // ... need to be able to change that dynamically.
    [value]
  );

  return debouncedValue;
}

export function SearchResults() {
  const { searchQuery } = useParams();
  const { data } = useQuery(ALL_SEARCH, {
    variables: { name: searchQuery }
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
    <div>
      {searchQuery && data && (
        <SimpleTabs
          startTabIdx={startTabIdx}
          tabs={[
            {
              label: `Legislators (${data.legislators.totalCount})`,
              content: (
                <div>
                  <LegislatorList data={data.legislators} hidePagination />
                </div>
              )
            },
            {
              label: `Donors (${data.donors.totalCount})`,
              content: (
                <div>
                  <DonorList data={data.donors} hidePagination />
                </div>
              )
            },
            {
              label: `Bills (${data.bills.totalCount})`,
              content: (
                <div>
                  <BillList data={data.bills} hidePagination />
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
  const [searchVal, setSearchVal] = useState("");
  const debouncedSearchTerm = useDebounce(searchVal, 500);
  const history = useHistory();
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
    <div style={{ margin: "1em 0" }}>
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
