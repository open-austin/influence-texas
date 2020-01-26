import React from "react";
import { useParams } from "react-router-dom";
import { useQuery } from "@apollo/react-hooks";
import { gql } from "apollo-boost";
import PaginatedList from "./PaginatedList";
import { format } from "date-fns";
import SimpleTabs from "./SimpleTabs";
import LegislatorsList from "./LegislatorList";
import CustomLink from "./CustomLink";
import { BillSquare } from "../styles";
import { Typography, Button } from "@material-ui/core";
import OpenInNewIcon from "@material-ui/icons/OpenInNew";

const GET_BILL = gql`
  query Bill($id: Int!) {
    bill(pk: $id) {
      chamber
      billId
      title
      billText
      session
      subjects {
        edges {
          node {
            label
          }
        }
      }
      sponsors {
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
      actionDates {
        totalCount
        edges {
          node {
            classification
            description
            date
          }
        }
      }
    }
  }
`;

function BillDetailPage() {
  const { id } = useParams();
  const { data } = useQuery(GET_BILL, {
    variables: { id }
  });
  const fullBillData = data ? data.bill : {};

  return (
    <div>
      <CustomLink to="/bills"> ← All Bills</CustomLink>

      <div style={{ display: "flex", margin: "1em 0" }}>
        <BillSquare billId={fullBillData.billId} />
        <div style={{ margin: "0 1em", flexGrow: 1 }}>
          <Typography variant="h5">{fullBillData.billId}</Typography>
          <div style={{ textTransform: "capitalize" }}>
            {fullBillData.chamber && fullBillData.chamber.toLowerCase()}
          </div>
          <div>Session {fullBillData.session}</div>
        </div>
        <Button
          variant="outlined"
          color="primary"
          size="small"
          href={fullBillData.billText}
          target="_blank"
          style={{ height: "fit-content" }}
        >
          <OpenInNewIcon fontSize="small" />{" "}
          <Typography variant="h6">Full Bill Text</Typography>
        </Button>
      </div>
      <div style={{ margin: "1em 0" }}>{fullBillData.title}</div>
      <div style={{ textTransform: "capitalize" }}>
        {" "}
        {fullBillData.subjects &&
          fullBillData.subjects.edges.map(d => {
            const [subject, parens] = d.node.label
              .replace(/--/g, "—")
              .toLowerCase()
              .split("(");
            return (
              <span key={d.node.label}>
                {subject} <span style={{ opacity: 0.5 }}>({parens} </span>
              </span>
            );
          })}
      </div>
      <SimpleTabs
        tabs={[
          {
            label: `Actions (${fullBillData.actionDates &&
              fullBillData.actionDates.totalCount})`,
            content: (
              <PaginatedList
                data={fullBillData.actionDates}
                title="Actions"
                className="no-scroll"
                columns={[
                  {
                    field: "node.description",
                    render: rowData => (
                      <div style={{ textTransform: "capitalize" }}>
                        <div
                          style={{
                            textTransform: "uppercase",
                            opacity: 0.5
                          }}
                        >
                          {rowData.node.classification.replace(/-/g, " ")}
                        </div>
                        <div>{rowData.node.description}</div>
                      </div>
                    )
                  },
                  {
                    field: "node.date",
                    render: rowData => (
                      <div style={{ textAlign: "right" }}>
                        {format(new Date(rowData.node.date), "PP")}
                      </div>
                    )
                  }
                ]}
                rowsPerPage={100}
              />
            )
          },
          {
            label: `Sponsors (${fullBillData.sponsors &&
              fullBillData.sponsors.totalCount})`,
            content: (
              <div className="detail-page">
                <LegislatorsList
                  data={fullBillData.sponsors}
                  title="Sponsors"
                  rowsPerPage={100}
                />
              </div>
            )
          }
        ]}
      />
    </div>
  );
}

export default BillDetailPage;
