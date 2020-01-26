import React from "react";
import { useParams } from "react-router-dom";
import { useQuery } from "@apollo/react-hooks";
import { gql } from "apollo-boost";
import { ImageSquare } from "../styles";
import { Typography, Button } from "@material-ui/core";
import OpenInNewIcon from "@material-ui/icons/OpenInNew";
import SimpleTabs from "./SimpleTabs";
import PaginatedList from "./PaginatedList";
import BillList from "./BillList";
import TexasDistrictMap from "./TexasDistrictMap";
import CustomLink from "./CustomLink";
import { formatMoney } from "../utils";

const GET_LEG = gql`
  query Legislator($id: Int!) {
    legislator(pk: $id) {
      pk
      name
      party
      chamber
      photoUrl
      url
      district
      contributions {
        edges {
          node {
            cycleTotal
            donor {
              pk
              fullName
            }
          }
        }
      }
      billsSponsored {
        totalCount
        edges {
          node {
            pk
            billId
            title
          }
        }
      }
    }
  }
`;

function LegislatorDetailPage() {
  const { id } = useParams();
  const { data } = useQuery(GET_LEG, {
    variables: { id }
  });
  const fullLegData = data ? data.legislator : {};
  return (
    <div className="detail-page">
      <CustomLink to="/legislators"> ← All Legislators</CustomLink>
      <div style={{ display: "flex", margin: "1em 0" }}>
        <ImageSquare photoUrl={fullLegData.photoUrl} />
        <div style={{ margin: "0 1em", flexGrow: 1 }}>
          <Typography variant="h5">{fullLegData.name}</Typography>
          <div style={{ textTransform: "capitalize" }}>
            {fullLegData.chamber && fullLegData.chamber.toLowerCase()} (
            {fullLegData.party})
          </div>
          <div>District {fullLegData.district}</div>
        </div>
        <Button
          variant="outlined"
          color="primary"
          size="small"
          href={fullLegData.url}
          target="_blank"
          style={{ height: "fit-content" }}
        >
          <OpenInNewIcon fontSize="small" />{" "}
          <Typography variant="h6">Full Biography</Typography>
        </Button>
      </div>

      <SimpleTabs
        tabs={[
          {
            label: `Bills Sponsored (${fullLegData.billsSponsored &&
              fullLegData.billsSponsored.totalCount})`,
            content: (
              <div>
                <BillList
                  title="Bills Sponsored"
                  data={fullLegData.billsSponsored}
                  rowsPerPage={100}
                />
              </div>
            )
          },
          {
            label: `Top Donors (${data &&
              fullLegData.contributions.edges.length})`,
            content: (
              <div>
                <PaginatedList
                  url="donors/donor"
                  pk="node.donor.pk"
                  title="Top Donors"
                  data={fullLegData.contributions}
                  columns={[
                    { field: "node.donor.fullName" },
                    {
                      render: rowData => {
                        return (
                          <div style={{ textAlign: "right" }}>
                            {formatMoney(rowData.node.cycleTotal)}
                          </div>
                        );
                      }
                    }
                  ]}
                  rowsPerPage={100}
                />
              </div>
            )
          },
          {
            label: "District Map",
            content: (
              <div>
                <TexasDistrictMap
                  chamber={fullLegData.chamber}
                  district={fullLegData.district}
                />
              </div>
            )
          }
        ]}
      />
    </div>
  );
}

export default LegislatorDetailPage;
