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
                <div style={{ marginLeft: "1rem"}}>
                  {rowData.node.fullName}
                  <div style={{ opacity: 0.5 }}>
                    {rowData.node.occupation}
                    {rowData.node.occupation && rowData.node.employer && " ・ "}
                    {rowData.node.employer}
                  </div>
                </div>
              </div>
            ),
          },
          {
            render: (rowData) => (
              <div style={{ textAlign: "right" }}>
                {formatMoney(rowData.node.totalContributions)}
                <div style={{ opacity: 0.5 }}>
                  {rowData.node.city}, {rowData.node.state}
                </div>
              </div>
            ),
          },
        ]}
      />
    </div>
  );
}

export default DonorList;
