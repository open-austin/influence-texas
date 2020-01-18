import React from "react";
import styled from "styled-components";

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
