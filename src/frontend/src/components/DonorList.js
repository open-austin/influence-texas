import React from "react";
import PaginatedList from "./PaginatedList";
import { RoundSquare } from "../styles";
import { Typography } from "@material-ui/core";
import { formatMoney } from "../utils";

function DonorList({ data, ...props }) {
  return (
    <div>
      <PaginatedList
        {...props}
        url="donors/donor"
        data={data}
        emptyState={<div>No donors found</div>}
        columns={[
          {
            field: "node.short_name",
            render: rowData => (
              <div style={{ display: "flex" }}>
                <RoundSquare>
                  {rowData.node.fullName[0] +
                    rowData.node.fullName.split(" ")[1][0]}
                </RoundSquare>
                <div style={{ margin: "0 1em" }}>
                  <Typography>{rowData.node.fullName}</Typography>
                  <Typography variant="subtitle2">
                    {rowData.node.employer}
                  </Typography>
                  <Typography variant="subtitle2">
                    {rowData.node.city}, {rowData.node.state}
                  </Typography>
                </div>
              </div>
            )
          },
          {
            render: rowData => (
              <div style={{ textAlign: "right" }}>
                {formatMoney(rowData.node.totalContributions)}
              </div>
            )
          }
        ]}
      />
    </div>
  );
}

export default DonorList;
