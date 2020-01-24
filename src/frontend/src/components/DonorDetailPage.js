import React from "react";
import { useParams } from "react-router-dom";
import { useQuery } from "@apollo/react-hooks";
import { gql } from "apollo-boost";
import PaginatedList from "./PaginatedList";
import { formatMoney } from "../utils";
import CustomLink from "./CustomLink";

const GET_DONOR = gql`
  query Donor($id: Int!) {
    donor(pk: $id) {
      fullName
      totalContributions
      city
      state
      donorsummarys {
        edges {
          node {
            cycleTotal
            filer {
              id
              office
              candidateName
              legislator {
                name
                pk
                district
                party
              }
            }
          }
        }
      }
    }
  }
`;

function DonorDetailPage() {
  const { id } = useParams();
  const { data } = useQuery(GET_DONOR, {
    variables: { id }
  });
  const fullDonorData = data ? data.donor : {};
  return (
    <div className="detail-page">
      <CustomLink to="/donors"> ← All Donors</CustomLink>
      <h1>{fullDonorData.fullName}</h1>
      <div>
        Total Contributions: {formatMoney(fullDonorData.totalContributions)}
      </div>
      <div>
        {fullDonorData.city}, {fullDonorData.state}
      </div>
      <PaginatedList
        url="legislators/legislator"
        pk="node.filer.legislator.pk"
        data={fullDonorData.donorsummarys}
        columns={[
          { field: "node.filer.candidateName" },
          { field: "node.filer.office", title: "Office" },
          {
            render: rowData => (
              <div style={{ textAlign: "right" }}>
                {formatMoney(rowData.node.cycleTotal)}
              </div>
            )
          }
        ]}
        rowsPerPage={100}
      />
    </div>
  );
}

export default DonorDetailPage;
