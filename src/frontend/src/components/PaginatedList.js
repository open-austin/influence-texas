import React, { useState } from "react";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableRow from "@material-ui/core/TableRow";
import { IconButton, Typography } from "@material-ui/core";
import ChevronLeft from "@material-ui/icons/ChevronLeft";
import ChevronRight from "@material-ui/icons/ChevronRight";
import styled from "styled-components";
import { useHistory } from "react-router-dom";

const StyleWrapper = styled.div`
  margin-left: -1em;
  width: calc(100% + 2em);
`;

function getProp(obj, propName) {
  if (!propName) {
    return;
  }
  if (propName.includes(".")) {
    return propName.split(".").reduce((o, i) => o && o[i], obj);
  }
  return obj[propName];
}
const zeroPageInfo = { first: null, last: null, before: null, after: null };

export default function PaginatedList({
  data = { edges: [], totalCount: 0 },
  columns,
  handleChangePage,
  url,
  pk = "node.pk",
  emptyState = "None found",
  title = "",
  sortOrderText = "",
  hidePagination = false,
  rowsPerPage = 10
}) {
  const { edges, totalCount, pageInfo } = data;
  const rows = edges;
  const { hasNextPage, endCursor } = pageInfo || {};
  const history = useHistory();
  const [lastPageInfo, setLastPageInfo] = useState([
    { ...zeroPageInfo, first: rowsPerPage }
  ]);
  if (emptyState && edges.length === 0) {
    return <div>{emptyState}</div>;
  }
  return (
    <StyleWrapper>
      <TableContainer>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            margin: "0 1em"
          }}
        >
          <Typography variant="h6">
            {title}
            <span
              variant="subtitle2"
              style={{ fontSize: ".75em", opacity: 0.5, margin: "1em" }}
            >
              {totalCount && `${totalCount} Results`}
            </span>
          </Typography>

          <Typography variant="h6">{sortOrderText}</Typography>
        </div>
        <Table aria-label="simple table">
          <TableBody>
            {rows.map((row, i) => (
              <TableRow
                key={getProp(row, pk) || i}
                hover={!!url}
                onClick={
                  url &&
                  pk &&
                  getProp(row, pk) &&
                  (e => history.push(`/${url}/${getProp(row, pk)}`))
                }
              >
                {columns.map((c, i) => {
                  if (c.render) {
                    return <TableCell key={i}>{c.render(row)}</TableCell>;
                  } else {
                    return (
                      <TableCell key={i}>{getProp(row, c.field)}</TableCell>
                    );
                  }
                })}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      {totalCount > rowsPerPage && !hidePagination && (
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignContent: "baseline"
          }}
        >
          <div style={{ padding: "1em 0" }}>{totalCount} Results </div>
          <div>
            <IconButton
              aria-label="Previous page"
              children={<ChevronLeft />}
              disabled={!lastPageInfo[1]}
              onClick={() => {
                handleChangePage(lastPageInfo[lastPageInfo.length - 2]);
                const newLastPageInfo = lastPageInfo.slice(0, -1);
                setLastPageInfo(newLastPageInfo);
              }}
              title="Previous page"
            />
            <IconButton
              aria-label="Next page"
              children={<ChevronRight />}
              disabled={!hasNextPage}
              onClick={() => {
                const pageInfo = {
                  ...zeroPageInfo,
                  after: endCursor,
                  first: rowsPerPage
                };
                handleChangePage(pageInfo);
                setLastPageInfo([...lastPageInfo, pageInfo]);
              }}
              title="Next page"
            />
          </div>
        </div>
      )}
    </StyleWrapper>
  );
}
