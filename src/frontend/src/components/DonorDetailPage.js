import React from "react";
import { useParams } from "react-router-dom";
import { useQuery } from "@apollo/react-hooks";
import { gql } from "apollo-boost";
import PaginatedList, { ShortLoadingListBody } from "./PaginatedList";
import { formatMoney, getDebugQuery } from "../utils";
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
      donations {
        cycleTotal
        candidateName
        office
        party
        legId
      }
    }
    ${getDebugQuery()}
  }
`;

function DonorDetailPage() {
  const { id } = useParams();
  const { data, loading, error } = useQuery(GET_DONOR, {
    variables: { id },
  });
  if (error) {
    return "server error";
  }
  const fullDonorData = data ? data.donor : {};
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
        {fullDonorData.occupation}{" "}
        {fullDonorData.occupation && fullDonorData.employer && "at"}{" "}
        {fullDonorData.employer}
        <div>
          {fullDonorData.city}, {fullDonorData.state}
        </div>
      </section>
      <PaginatedList
        url="legislators/legislator"
        pk="legId"
        data={
          loading
            ? null
            : {
                edges: fullDonorData.donations,
                totalCount: fullDonorData.donations.length,
              }
        }
        columns={[
          {
            render: (rowData) => (
              <div style={{ display: "flex" }}>
                <RoundSquare
                  style={{
                    marginTop: 10,
                    width: 20,
                    height: 20,
                    background: rowData.legId
                      ? legTheme.palette.primary.main
                      : "#bbb",
                  }}
                />
                <div style={{ margin: "0 1em" }}>
                  <Typography>{rowData.candidateName}</Typography>
                  <Typography variant="subtitle2">
                    {rowData.office} {rowData.party ? `(${rowData.party})` : ""}
                  </Typography>
                </div>
              </div>
            ),
          },
          {
            render: (rowData) => (
              <div style={{ textAlign: "right" }}>
                {formatMoney(rowData.cycleTotal)}
              </div>
            ),
          },
        ]}
        showHover={(rowData) => !!rowData.legId}
        loading={loading}
        loadingListBody={ShortLoadingListBody}
        rowsPerPage={500}
      />
    </div>
  );
}

export default DonorDetailPage;
