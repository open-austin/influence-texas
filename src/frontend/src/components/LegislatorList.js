import React from "react";
import PaginatedList from "./PaginatedList";
import { ImageSquare } from "../styles";
import Typography from "@material-ui/core/Typography";
import { capitalize } from "../utils";

const PARTIES = {
  R: "Republican",
  D: "Democrat",
  I: "Independent",
};

export default function LegislatorsList({
  data,
  nestedUnder = "legislators",
  ...props
}) {
  return (
    <PaginatedList
      {...props}
      url="legislators/legislator"
      data={data}
      emptyState={<div>No legislators found</div>}
      nestedUnder={nestedUnder}
      columns={[
        {
          render: (rowData) => (
            <div style={{ display: "flex" }}>
              <ImageSquare photoUrl={rowData.node.photoUrl} />
              <div style={{ margin: "0 1em" }}>
                <Typography>{rowData.node.name}</Typography>
                <Typography variant="subtitle2">
                  {capitalize(rowData.node.chamber)}
                </Typography>
                <Typography variant="subtitle2">
                  {PARTIES[rowData.node.party] || rowData.node.party}
                </Typography>
              </div>
            </div>
          ),
        },
        {
          field: "node.party",
          render: (rowData) => (
            <div style={{ textAlign: "right" }}>
              District {rowData.node.district}
            </div>
          ),
        },
      ]}
    />
  );
}
