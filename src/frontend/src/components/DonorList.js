import React from "react";
import PaginatedList from "./PaginatedList";
import { RoundSquare } from "../styles";
import { Typography } from "@material-ui/core";
import { formatMoney } from "../utils";

function getInitials(name) {
  try {
    return name[0] + name.split(" ")[1][0];
  } catch (e) {
    return name && name[0];
  }
}

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
            render: (rowData) => (
              <div style={{ display: "flex" }}>
                <RoundSquare>{getInitials(rowData.node.fullName)}</RoundSquare>
                <div style={{ margin: "0 1em" }}>
                  <Typography>{rowData.node.fullName}</Typography>
                  {rowData.node.employer !== rowData.node.fullName && <Typography variant="subtitle2">
                    {rowData.node.employer}
                  </Typography>}
                  <Typography variant="subtitle2">
                    {rowData.node.city}, {rowData.node.state}
                  </Typography>
                </div>
              </div>
            ),
          },
          {
            render: (rowData) => (
              <div style={{ textAlign: "right" }}>
                {formatMoney(rowData.node.totalContributions)}
              </div>
            ),
          },
        ]}
      />
    </div>
  );
}

export default DonorList;
