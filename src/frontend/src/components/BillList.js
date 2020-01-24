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
        { field: "node.title" },
        { field: "node.chamber" }
      ]}
    />
  );
}

export default BillList;
