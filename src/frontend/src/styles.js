import React from "react";
import styled from "styled-components";

export const BlankLoadingLine = styled.div`
  background: #ddd;
  width: ${(p) => p.width || "100%"};
  height: 1em;
  margin-bottom: 1em;
`;

export const RoundSquare = styled.div`
  background: #ddd;
  border-radius: 5px;
  color: #888;
  font-size: 2em;
  width: 2.5em;
  height: 2.5em;
  line-height: 2.5em;
  text-align: center;
`;

export const ImageSquare = ({ photoUrl }) => (
  <RoundSquare
    style={{
      backgroundImage: `url(${photoUrl})`,
      backgroundSize: "cover"
    }}
  />
);

export const BillSquare = ({ billId = "" }) => {
  const [chamber, number] = billId.split(" ");

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
};
