import React from "react";
import { useParams } from "react-router-dom";
import { useQuery } from "@apollo/react-hooks";
import { gql } from "apollo-boost";
import PaginatedList from "./PaginatedList";
import { format } from "date-fns";
import SimpleTabs from "./SimpleTabs";
import LegislatorsList from "./LegislatorList";
import CustomLink from "./CustomLink";

const GET_BILL = gql`
  query Bill($id: Int!) {
    bill(pk: $id) {
      chamber
      billId
      title
      subjects {
        edges {
          node {
            label
          }
        }
      }
      sponsors {
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

      <h1>{fullBillData.billId}</h1>
      <div>{fullBillData.chamber}</div>
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
            label: "Actions",
            content: (
              <PaginatedList
                data={fullBillData.actionDates}
                title="Actions"
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
                rowsPerPage={50}
              />
            )
          },
          {
            label: "Sponsors",
            content: (
              <LegislatorsList
                data={fullBillData.sponsors}
                title="Sponsors"
                rowsPerPage={50}
              />
            )
          }
        ]}
      />
    </div>
  );
}

export default BillDetailPage;
