import React from "react";
import PaginatedList from "./PaginatedList";
import { BillSquare } from "../styles";

function BillList({ data, ...props }) {
  return (
    <PaginatedList
      {...props}
      url="bills/bill"
      data={data}
      emptyState={<div>No bills found</div>}
      columns={[
        {
          render: rowData => <BillSquare billId={rowData.node.billId} />
        },
        {
          render: rowData => (
            <div>
              <span style={{ opacity: 0.5 }}>Relating to</span>
              {rowData.node.title.replace("Relating to", "")}
            </div>
          )
        },
        { field: "node.chamber" }
      ]}
    />
  );
}

export default BillList;
