import React from "react";
import DonorList from "./DonorList";
import { useQuery } from "@apollo/react-hooks";
import { gql } from "apollo-boost";

const ALL_DONORS = gql`
  query AllDonors($first: Int, $last: Int, $after: String, $before: String) {
    donors(first: $first, last: $last, after: $after, before: $before) {
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

function DonorsPage() {
  const { data } = useQuery(ALL_DONORS);
  return (
    <div>
      <DonorList data={data && data.donors} title="Donors" />
    </div>
  );
}

export default DonorsPage;
