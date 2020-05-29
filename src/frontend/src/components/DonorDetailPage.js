import React from "react";
import { useParams } from "react-router-dom";
import { useQuery } from "@apollo/react-hooks";
import { gql } from "apollo-boost";
import PaginatedList, { ShortLoadingListBody } from "./PaginatedList";
import { formatMoney } from "../utils";
import CustomLink from "./CustomLink";
import { BlankLoadingLine } from "../styles";
import { RoundSquare } from "../styles";
import Typography from "@material-ui/core/Typography";
import { legTheme } from "../theme";

const GET_DONOR = gql`
  query Donor($id: Int!) {
    donor(pk: $id) {
      fullName
      totalContributions
      city
      state
      employer
      occupation
      donorsummarys {
        totalCount
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
  const { data, loading } = useQuery(GET_DONOR, {
    variables: { id },
  });
  const fullDonorData = data ? data.donor : {};
  let donorsummarys = fullDonorData.donorsummarys;
  if (!loading) {
    donorsummarys.edges.sort(
      (d1, d2) => d2.node.cycleTotal - d1.node.cycleTotal
    );
  }
  return (
    <div className="detail-page">
      <CustomLink to="/donors"> ← All Donors</CustomLink>
      <section style={{ margin: "1rem" }}>
        <h1>
          {loading ? <BlankLoadingLine width="40%" /> : fullDonorData.fullName}
        </h1>
        <div>
          {loading ? (
            <BlankLoadingLine width="20%" />
          ) : (
            `Total Contributions: ${formatMoney(
              fullDonorData.totalContributions
            )}`
          )}
        </div>
        {fullDonorData.occupation} {fullDonorData.occupation && fullDonorData.employer && 'at'}{' '}
        {fullDonorData.employer}
        <div>
          {fullDonorData.city}, {fullDonorData.state}
        </div>
      </section>
      <PaginatedList
        url="legislators/legislator"
        pk="node.filer.legislator.pk"
        data={donorsummarys}
        columns={[
          {
            render: (rowData) => (
              <div style={{ display: "flex" }}>
                <RoundSquare
                  style={{
                    marginTop: 10,
                    width: 20,
                    height: 20,
                    background: rowData.node.filer.legislator
                      ? legTheme.palette.primary.main
                      : "#bbb",
                  }}
                />
                <div style={{ margin: "0 1em" }}>
                  <Typography>{rowData.node.filer?.candidateName}</Typography>
                  <Typography variant="subtitle2">
                    {rowData.node.filer?.office}{" "}
                    {rowData.node.filer.legislator
                      ? `(${rowData.node.filer.legislator.party})`
                      : ""}
                  </Typography>
                </div>
              </div>
            ),
          },
          {
            render: (rowData) => (
              <div style={{ textAlign: "right" }}>
                {formatMoney(rowData.node.cycleTotal)}
              </div>
            ),
          },
        ]}
        showHover={(rowData) => !!rowData.node.filer.legislator}
        loading={loading}
        loadingListBody={ShortLoadingListBody}
        rowsPerPage={500}
      />
    </div>
  );
}

export default DonorDetailPage;
