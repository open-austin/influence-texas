import React from "react";
import { Typography } from "@material-ui/core";
import styled from "styled-components";
import { Link } from "react-router-dom";

const LogoWrapper = styled.header`
  text-transform: uppercase;
  && {
    color: black;
  }
  &&,
  p {
    font-size: 2rem !important;
    display: inline-block;
    font-weight: bold;
  }
`;

export default function Logo() {
  return (
    <Link to="/">
      <LogoWrapper>
        <Typography color="primary">Influence</Typography> Texas
      </LogoWrapper>
    </Link>
  );
}
