import React from "react";
import PaginatedList from "./PaginatedList";
import { RoundSquare } from "../styles";

function BillList({ data, ...props }) {
  return (
    <PaginatedList
      {...props}
      url="bills/bill"
      data={data}
      emptyState={<div>No bills found</div>}
      columns={[
        {
          field: "node.billId",
          render: rowData => {
            const [chamber, number] = rowData.node.billId.split(" ");

            return (
              <RoundSquare>
                <div
                  style={{
                    lineHeight: 1,
                    paddingTop: ".5em"
                  }}
                >
                  {chamber}
                </div>
                <div style={{ fontSize: ".6em", lineHeight: 1 }}>{number}</div>
              </RoundSquare>
            );
          }
        },
        { field: "node.title" },
        { field: "node.chamber" }
      ]}
    />
  );
}

export default BillList;
